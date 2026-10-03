# Anno

**Anno** is a Catholic-first native SwiftUI devotional and pilgrimage app built around deterministic calendar math, sourced historical research, and a deliberately narrow v1.

## v1 product

- **Daily devotional:** EN-primary Catholic devotional content backed by structured research and source references.
- **Deterministic calendar engine:** Engine A converts Gregorian dates across the supported liturgical/calendar systems without using an LLM for date math.
- **Five flagship pilgrimage routes:** Orange County / Our Lady of La Vang (featured exemplar), Jerusalem / Holy Land, Rome Seven Churches, Camino de Santiago, and Our Lady of Guadalupe.
- **Focused localization:** English is primary; Vietnamese is required for the selected major feasts defined in the current product docs.
- **Two tiers:** Free + Premium ($49.99/year).

The following are **not v1 features**: AR reliquaries, spatial/geofenced audio, the interfaith layer, the old 72-sanctuary browsing surface, and the broader 18-route catalog. Prior work is preserved under `archive/v1-removed/` where useful.

## Current implementation state

- Engine A lives at `calendar_engine.py` with validation/tests under `tools/`.
- Engine B research generation and validation live under `tools/` and `docs/research/`.
- The normalized 2026 app fixture is `Anno/Resources/anno_unified_2026.json`.
- The v1 pilgrimage source of truth is `Anno/Resources/flagship_routes_v1.json`; the app loader resolves those five route files directly.
- The native client lives under `Anno/` and is generated from `Anno/project.yml` with XcodeGen.
- Cheap GitHub Actions validate engines/content/routes on pushes. Native macOS/Xcode validation is intentionally manual/opt-in to avoid accidental runner-minute burn.

## Repository map

```text
.
├── Anno/                         # Native SwiftUI application
│   ├── Models/
│   ├── Services/
│   ├── Today/
│   ├── Map/
│   ├── Resources/
│   │   ├── anno_unified_2026.json
│   │   ├── flagship_routes_v1.json
│   │   └── PilgrimageRoutes/
│   └── project.yml              # XcodeGen project spec
├── calendar_engine.py           # Engine A deterministic calendar conversion
├── tools/                       # Engine B, normalization, export, validation
├── data/                        # Generated/research pipeline data
├── docs/                        # Product, research, build, and architecture docs
└── archive/v1-removed/          # Preserved features intentionally deferred from v1
```

## Canonical project docs

Read these before extending the product:

1. `START_HERE.md` — canonical orientation and scope.
2. `PRD.md` — current product definition.
3. `ROADMAP.md` — current delivery state and next phases.
4. `ARCHITECTURE.md` — active architecture and boundaries.
5. `docs/HANDOFF_2026-10-03.md` — exact pause/resume state.
6. `docs/NATIVE_BUILD_RUNBOOK.md` — native build and TestFlight path.
7. `AGENTS.md` — repository instructions and invariants.

When older documents disagree with these, treat `START_HERE.md`, the current root docs above, and Issues #28/#31/#33 as authoritative.

## Useful validation commands

```bash
python3 tools/test_calendar_engine.py
python3 tools/validate_engine_b_output.py --help
python3 tools/validate_sanctuaries.py
python3 tools/validate_route_coordinates.py
```

Native project generation requires macOS/Xcode:

```bash
cd Anno
xcodegen generate
```

The immediate shipping goal is simple: **get the narrow v1 building cleanly, render the real normalized devotional content, and make the five pilgrimage routes work end-to-end before restoring any deferred feature.**
