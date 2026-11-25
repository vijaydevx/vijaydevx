#!/usr/bin/env python3
"""Render Vijay's profile identity and project card using the bundled fonts."""
import html
import os
from font_faces import embedded_font_faces

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "info-card.svg")

projects = [
    ("AVNEXAI", "AI-powered network intelligence platform", "#53d5c6"),
    ("NEXORA", "AI website builder and motion-rich web experience", "#a994ff"),
    ("ROYBOT", "ESP32 self-balancing robot prototype and dashboard", "#ffc17e"),
    ("VERTO", "Campus lost-and-found platform", "#83d7a5"),
    ("MEETRIC", "Project repository — details to be added", "#cfb8ff"),
    ("C PROGRAMMING", "Daily C practice through data structures", "#77d2e5"),
]

parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="840" height="880" viewBox="0 0 840 880" role="img" aria-labelledby="title desc">',
    '<title id="title">Vijay Anand — profile and projects</title>',
    '<desc id="desc">ECE, RHCSA, Linux, networking, cloud and DevOps projects</desc>',
    f'<style>{embedded_font_faces()}</style>',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0d1420"/><stop offset="1" stop-color="#142338"/></linearGradient><linearGradient id="shine"><stop stop-color="#50d7c7"/><stop offset="1" stop-color="#92a9ff"/></linearGradient></defs>',
    '<rect width="840" height="880" rx="18" fill="url(#bg)"/><rect x="1" y="1" width="838" height="878" rx="17" fill="none" stroke="#354a5c"/>',
    '<text x="40" y="54" fill="#59d5c9" font-family="Geist Mono" font-size="13" letter-spacing="2">ECE  /  RHCSA  /  LINUX</text>',
    '<text x="36" y="125" fill="#f1f5f9" font-family="Instrument Serif" font-size="58">Vijay Anand</text>',
    '<text x="40" y="165" fill="#c5d2df" font-family="Geist" font-size="17">Exploring Linux, networks, cloud infrastructure and DevOps.</text>',
    '<rect x="40" y="192" width="760" height="1" fill="#34495d"/>',
    '<text x="40" y="235" fill="#93a4b5" font-family="Geist Mono" font-size="12" letter-spacing="2">SELECTED BUILDS</text>',
]

for index, (name, description, accent) in enumerate(projects):
    col, row = index % 2, index // 2
    x, y = 40 + col * 390, 260 + row * 178
    safe_name, safe_description = html.escape(name), html.escape(description)
    parts.extend([
        f'<rect x="{x}" y="{y}" width="370" height="154" rx="13" fill="#121e2c" stroke="#2c4052"/>',
        f'<rect x="{x + 20}" y="{y + 22}" width="7" height="7" rx="2" fill="{accent}"/>',
        f'<text x="{x + 40}" y="{y + 31}" fill="#f1f5f9" font-family="Geist" font-weight="600" font-size="17">{safe_name}</text>',
        f'<text x="{x + 20}" y="{y + 74}" fill="#bdcad7" font-family="Geist" font-size="13">{safe_description}</text>',
        f'<text x="{x + 20}" y="{y + 127}" fill="{accent}" font-family="Geist Mono" font-size="11">GITHUB  ↗</text>',
    ])

parts.extend([
    '<rect x="40" y="808" width="760" height="1" fill="#34495d"/>',
    '<text x="40" y="842" fill="#93a4b5" font-family="Geist Mono" font-size="12">NETWORKS  ·  CLOUD  ·  DEVOPS</text>',
    '<text x="800" y="842" fill="url(#shine)" font-family="Geist Mono" font-size="12" text-anchor="end">github.com/vijaydevx</text>',
    '</svg>',
])

with open(OUT, "w", encoding="utf-8") as output_file:
    output_file.write("".join(parts))
print(f"wrote {OUT}")
