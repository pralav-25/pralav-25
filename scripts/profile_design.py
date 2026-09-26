#!/usr/bin/env python3
"""Render the profile's editorial artwork locally, without API calls or fonts."""

import argparse
from html import escape
from pathlib import Path

THEMES = {
    "dark": {
        "bg": "#10161b",
        "ink": "#f4f5ed",
        "muted": "#a8b5b6",
        "line": "#2b373c",
        "accent": "#d6f369",
        "panel": "#1a252a",
    },
    "light": {
        "bg": "#f4f5ee",
        "ink": "#182822",
        "muted": "#56685e",
        "line": "#ced7ca",
        "accent": "#426019",
        "panel": "#e6ebdd",
    },
}
FONT = "Arial, Helvetica, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, monospace"


def svg(width, height, title, description, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(description)}</desc>\n'
        f'<g font-family="{FONT}">{body}</g>\n</svg>\n'
    )


def hero(theme):
    t = THEMES[theme]
    lines = "".join(f'<path d="M{x} 0v360"/>' for x in range(720, 1121, 40))
    lines += "".join(f'<path d="M720 {y}h400"/>' for y in range(0, 361, 40))
    return svg(
        1120,
        360,
        "Pralav Singh — Data. Code. Things that work.",
        "Python, data science and machine learning. Open to internships. A geometric data-to-software illustration accompanies the introduction.",
        f'''
<defs><clipPath id="frame"><rect width="1120" height="360" rx="20"/></clipPath></defs>
<g clip-path="url(#frame)">
<rect width="1120" height="360" fill="{t["bg"]}"/>
<g fill="none" stroke="{t["line"]}" opacity=".65">{lines}</g>
<circle cx="972" cy="182" r="161" fill="{t["accent"]}" opacity=".07"/>
<path d="M46 52h26" stroke="{t["accent"]}" stroke-width="4"/>
<text x="86" y="57" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{t["muted"]}">PYTHON BUILDER / INDIA</text>
<text x="44" y="142" font-size="76" font-weight="700" letter-spacing="-3.5" fill="{t["ink"]}">Pralav Singh<tspan fill="{t["accent"]}">.</tspan></text>
<text x="48" y="200" font-size="32" font-weight="600" letter-spacing="-.7" fill="{t["ink"]}">Data. Code. Things that work.</text>
<text x="48" y="235" font-size="20" fill="{t["muted"]}">Machine learning, useful APIs, and interactive experiments.</text>
<rect x="46" y="276" width="455" height="40" rx="20" fill="{t["panel"]}" stroke="{t["line"]}"/>
<circle cx="67" cy="296" r="5" fill="{t["accent"]}"/>
<text x="84" y="301" font-family="{MONO}" font-size="13" letter-spacing=".4" fill="{t["ink"]}">OPEN TO DATA SCIENCE + ML INTERNSHIPS</text>
<g fill="none" stroke="{t["accent"]}" stroke-width="1.5">
<path d="m877 89 120 69v112l-120-69z" fill="{t["panel"]}"/>
<path d="m877 89-75 44v112l75-44m-75-68 120 69 75-44m-75 44v112l-120-69m120 69 75-44"/>
<path d="m827 148 120 69m-96-83 120 69m-94-87v113m24-99v113m23-99v113" opacity=".25"/>
<circle cx="877" cy="89" r="5" fill="{t["accent"]}"/>
<circle cx="802" cy="245" r="5" fill="{t["accent"]}"/>
<circle cx="997" cy="158" r="5" fill="{t["accent"]}"/>
</g>
<rect x="948" y="54" width="120" height="37" rx="8" fill="{t["accent"]}"/>
<text x="1008" y="78" font-family="{MONO}" font-size="17" text-anchor="middle" fill="{t["bg"]}">build()</text>
<rect x="762" y="287" width="138" height="32" rx="7" fill="{t["panel"]}" stroke="{t["line"]}"/>
<text x="831" y="309" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["ink"]}">idea → demo</text>
</g>
<rect x=".5" y=".5" width="1119" height="359" rx="20" fill="none" stroke="{t["line"]}"/>
''',
    )


FEATURES = {
    "shiftwatch": (
        "01",
        "MODELS + MONITORING",
        "#b4b6fc",
        "#4b4291",
        "Two contrasting distribution curves represent monitoring changes in data.",
    ),
    "dataset-gate": (
        "02",
        "DATA QUALITY",
        "#d6f369",
        "#426019",
        "A table of checks passes through a data-quality gate.",
    ),
    "interleave": (
        "03",
        "INTERACTIVE SYSTEMS",
        "#f3b78e",
        "#8b432b",
        "Two worker traces cross and arrive at a shared state.",
    ),
    "structiq": (
        "04",
        "APIS + APPLICATIONS",
        "#89d4d7",
        "#225e68",
        "A bridge and mapped locations represent maintenance workspaces.",
    ),
}


def feature(name, theme):
    number, label, dark, light, description = FEATURES[name]
    t = THEMES[theme]
    color = dark if theme == "dark" else light
    drawings = {
        "shiftwatch": '<path d="M34 113h436M66 64v71" opacity=".3"/><path d="M67 112c46 0 50-56 88-56s43 56 92 56"/><path d="M183 112c47 0 58-67 99-67s51 67 119 67" stroke-dasharray="6 5"/><circle cx="155" cy="56" r="5"/><circle cx="282" cy="45" r="5"/>',
        "dataset-gate": '<rect x="74" y="53" width="145" height="76" rx="8"/><path d="M74 78h145m-97-25v76m49-76v76m-97-26h145" opacity=".35"/><path d="M247 91h54m-9-8 9 8-9 8"/><rect x="330" y="52" width="78" height="78" rx="15"/><path d="m348 91 14 14 29-32" stroke-width="4"/>',
        "interleave": '<path d="M56 65h113c44 0 61 51 102 51h155"/><path d="M56 116h114c42 0 62-51 104-51h152" stroke-dasharray="7 5"/><circle cx="108" cy="65" r="8"/><circle cx="319" cy="65" r="8"/><circle cx="371" cy="116" r="8"/><path d="M427 56v69"/>',
        "structiq": '<path d="M58 121h366M90 121V65m305 56V65M90 87h305M91 65q151 103 303 0M139 90v31m50-18v18m53-13v13m51-18v18m51-31v31"/><circle cx="91" cy="55" r="7"/><circle cx="394" cy="55" r="7"/>',
    }
    return svg(
        500,
        158,
        label.title(),
        description,
        f'''
<rect width="500" height="158" rx="12" fill="{t["panel"]}"/>
<rect x=".5" y=".5" width="499" height="157" rx="12" fill="none" stroke="{t["line"]}"/>
<text x="22" y="28" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.5" fill="{color}">{label}</text>
<text x="474" y="29" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{number}</text>
<g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{drawings[name]}</g>
''',
    )


def button(label, width, primary=False):
    fill, ink = ("#d6f369", "#182822") if primary else ("#1a252a", "#f4f5ed")
    return svg(
        width,
        40,
        label,
        f"Navigation link: {label}",
        f'''
<rect x=".5" y=".5" width="{width - 1}" height="39" rx="8" fill="{fill}" stroke="{fill}"/>
<text x="{width / 2}" y="25" text-anchor="middle" font-size="14" font-weight="700" fill="{ink}">{escape(label)}</text>
''',
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parents[1] / "assets"
    )
    output = parser.parse_args().out
    output.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (output / f"profile-hero-{theme}.svg").write_text(hero(theme), encoding="utf-8")
        for name in FEATURES:
            (output / f"feature-{name}-{theme}.svg").write_text(
                feature(name, theme), encoding="utf-8"
            )
    for name, label, width, primary in [
        ("portfolio", "Explore my portfolio ↗", 188, True),
        ("email", "Let's connect ↗", 142, False),
        ("demo", "Try ShiftWatch ↗", 155, False),
    ]:
        (output / f"link-{name}.svg").write_text(
            button(label, width, primary), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
