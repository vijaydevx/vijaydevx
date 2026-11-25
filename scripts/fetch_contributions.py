#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar and summarize its activity."""
import datetime
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen

USERNAME = os.environ.get("GH_PROFILE_USER", "vijaydevx")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


class ContributionCalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.tooltips = {}
        self.current_tooltip = None
        self.tooltip_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in attrs.get("class", "").split():
            date = attrs.get("data-date")
            if date:
                self.days.append({
                    "date": date,
                    "level": int(attrs.get("data-level") or 0),
                    "tooltip_id": attrs.get("id"),
                })
        elif tag == "tool-tip" and attrs.get("for"):
            self.current_tooltip = attrs["for"]
            self.tooltip_text = []

    def handle_data(self, data):
        if self.current_tooltip is not None:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.current_tooltip is not None:
            self.tooltips[self.current_tooltip] = " ".join(self.tooltip_text).strip()
            self.current_tooltip = None
            self.tooltip_text = []


def fetch_days():
    request = Request(URL, headers={"User-Agent": "profile-readme-bot/1.0"})
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", errors="replace")

    parser = ContributionCalendarParser()
    parser.feed(page)
    if not parser.days:
        print("No contribution calendar found; GitHub may have changed its markup.", file=sys.stderr)
        raise SystemExit(1)

    days = []
    for day in parser.days:
        tooltip = parser.tooltips.get(day["tooltip_id"], "")
        count_match = re.match(r"\s*(\d+)", tooltip)
        count = 0 if re.search(r"no contributions", tooltip, re.I) else int(count_match.group(1)) if count_match else 0
        days.append({"date": day["date"], "count": count, "level": day["level"]})
    return sorted(days, key=lambda item: item["date"])


def compute_current_streak(days):
    index = len(days) - 1
    if days[index]["count"] == 0:
        index -= 1
    end_index = index
    while index >= 0 and days[index]["count"] > 0:
        index -= 1
    start_index = index + 1
    length = end_index - start_index + 1
    if length <= 0:
        return {"length": 0, "start": None, "end": None}
    return {"length": length, "start": days[start_index]["date"], "end": days[end_index]["date"]}


def compute_longest_streak(days):
    best_length = run = 0
    best_start = best_end = None
    run_start = 0
    for index, day in enumerate(days):
        if day["count"] > 0:
            if run == 0:
                run_start = index
            run += 1
            if run > best_length:
                best_length = run
                best_start = days[run_start]["date"]
                best_end = day["date"]
        else:
            run = 0
    return {"length": best_length, "start": best_start, "end": best_end}


def build_data(days):
    total = sum(day["count"] for day in days)
    active_days = sum(day["count"] > 0 for day in days)
    best = max(days, key=lambda day: day["count"])
    monthly = {}
    for day in days:
        month = day["date"][:7]
        monthly[month] = monthly.get(month, 0) + day["count"]
    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": compute_current_streak(days),
        "longest_streak": compute_longest_streak(days),
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": [{"month": month, "total": count} for month, count in sorted(monthly.items())],
        "days": days,
    }


if __name__ == "__main__":
    contribution_data = build_data(fetch_days())
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as output_file:
        json.dump(contribution_data, output_file, indent=2)
    print(f"wrote {OUT_PATH}: {contribution_data['total_contributions']} contributions")
