#!/usr/bin/env python3
"""Generate printable QR field markers for the SoCal La Vang exemplar."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import qrcode
import qrcode.image.svg


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def svg_for(payload: str) -> str:
    image = qrcode.make(
        payload,
        image_factory=qrcode.image.svg.SvgPathImage,
        box_size=8,
        border=4,
    )
    output = Path("/tmp/anno-marker.svg")
    image.save(output)
    text = output.read_text()
    return text[text.index("<svg"):]


def write_svg(path: Path, payload: str) -> None:
    image = qrcode.make(
        payload,
        image_factory=qrcode.image.svg.SvgPathImage,
        box_size=8,
        border=4,
    )
    image.save(path)


def build_html(manifest: dict, output_dir: Path) -> str:
    cards = []

    for marker in manifest["markers"]:
        index = marker["marker_index"]
        payload = marker["payload"]
        label_en = html.escape(marker["label_en"])
        label_vi = html.escape(marker["label_vi"])
        svg = svg_for(payload)

        cards.append(
            f"""
            <article class="card">
              <div class="qr">{svg}</div>
              <div class="num">STATION {index}</div>
              <h2>{label_en}</h2>
              <p class="vi">{label_vi}</p>
              <p class="cta">Open in Anno · Mở trong Anno</p>
              <code>{html.escape(payload)}</code>
            </article>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Anno — La Vang Orange County Field Markers</title>
<style>
@page {{ size: letter; margin: 0.35in; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",sans-serif; background:#fff; color:#13110e; }}
header {{ padding:0 0 14px; text-align:center; }}
header h1 {{ margin:0 0 4px; font-family:Georgia,serif; font-size:24px; }}
header p {{ margin:0; font-size:11px; color:#665f54; }}
.grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }}
.card {{ min-height:3.35in; border:1.5px solid #c9a84c; border-radius:18px; padding:14px; text-align:center; page-break-inside:avoid; position:relative; overflow:hidden; }}
.card:before {{ content:""; position:absolute; width:150px; height:150px; border-radius:50%; background:rgba(29,48,88,.07); top:-75px; right:-55px; }}
.qr svg {{ width:1.55in; height:1.55in; display:block; margin:0 auto 8px; }}
.num {{ font-size:9px; font-weight:800; letter-spacing:1.5px; color:#9a7d2f; }}
h2 {{ font-family:Georgia,serif; font-size:17px; margin:5px 0 3px; line-height:1.08; }}
.vi {{ font-family:Georgia,serif; font-size:12px; margin:0 0 10px; color:#4f493f; }}
.cta {{ font-size:10px; font-weight:700; margin:7px 0 4px; }}
code {{ font-size:8px; color:#777; }}
footer {{ margin-top:10px; font-size:9px; color:#777; text-align:center; }}
</style>
</head>
<body>
<header>
<h1>Anno · Our Lady of La Vang — Orange County Pilgrimage</h1>
<p>Temporary field-test markers · QR/NFC identities share one Anno deep-link system</p>
</header>
<section class="grid">
{''.join(cards)}
</section>
<footer>Field-test only. Do not install at a parish/shrine without site permission.</footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="Anno/Resources/socal_la_vang_physical_markers_v1.json",
    )
    parser.add_argument(
        "--output",
        default="build/socal-la-vang-field-markers",
    )
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for marker in manifest["markers"]:
        index = marker["marker_index"]
        station_id = marker["station_id"]
        payload = marker["payload"]
        write_svg(
            output_dir / f"{index:02d}-{station_id}.svg",
            payload,
        )

    (output_dir / "print-sheet.html").write_text(
        build_html(manifest, output_dir)
    )

    (output_dir / "README.txt").write_text(
        "Anno SoCal La Vang field-test markers\n"
        "Open print-sheet.html and print at 100% scale.\n"
        "Do not install physical markers at a parish or shrine without permission.\n"
    )

    print(f"generated {len(manifest['markers'])} markers in {output_dir}")


if __name__ == "__main__":
    main()
