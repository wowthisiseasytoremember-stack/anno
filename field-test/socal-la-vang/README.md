# SoCal La Vang physical-marker field test

The canonical marker identities live in:

`Anno/Resources/socal_la_vang_physical_markers_v1.json`

Generate the printable kit with:

```bash
python3 -m pip install qrcode
python3 tools/generate_socal_field_markers.py
```

Output:

- seven SVG QR markers
- one printable HTML sheet
- a short field-test README

Compact marker payloads:

- `anno://p/lv/1` — Our Lady of La Vang Shrine
- `anno://p/lv/2` — 117 Vietnamese Martyrs
- `anno://p/lv/3` — Marian Gardens
- `anno://p/lv/4` — Saint Columban
- `anno://p/lv/5` — Vietnamese Catholic Center
- `anno://p/lv/6` — Our Lady of La Vang Catholic Church
- `anno://p/lv/7` — Saint Barbara

The iPhone app resolves each compact marker to the canonical route/station ID.

## Precision model

- GPS: five geographic chapters
- QR/NFC: seven exact spiritual stations
- AR/Vision: exact physical object/context where appropriate
- manual **I'm Here**: always available

Do not install a marker at any church, shrine, or center without permission.
