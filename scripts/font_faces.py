"""Shared embedded font faces for the generated SVG profile graphics."""
import base64
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_FILES = (
    ("Instrument Serif", "normal", "serif-400.woff"),
    ("Geist", "normal", "geist-400.woff"),
    ("Geist", "600", "geist-600.woff"),
    ("Geist Mono", "normal", "geistmono-400.woff"),
)


def embedded_font_faces():
    rules = []
    for family, weight, filename in FONT_FILES:
        path = os.path.join(ROOT, "fonts", filename)
        with open(path, "rb") as font_file:
            encoded = base64.b64encode(font_file.read()).decode("ascii")
        rules.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:font/woff;base64,{encoded}) format('woff')}}"
        )
    return "".join(rules)
