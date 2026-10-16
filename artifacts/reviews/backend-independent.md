# Independent backend review

Synthetic fixture checks; no real apartment photograph accuracy claim. Run with `python scripts/critic_backend.py --serve` to test current on-disk code through a temporary real HTTP server, or `--url http://127.0.0.1:8765` for the app server.

38/38 probes pass; 0 findings.

- **PASS two-room-plan.png wall count** — 8 detected; visible source has eight segments
- **PASS two-room-plan.png independently matched endpoints** — max endpoint deviation=0.018m, tolerance 0.15m (known 8×6m centerline plan)
- **PASS two-room-plan.png calibration/no furniture** — width=8.0m, objects=0, height=2.7m
- **PASS two-room-plan.png warnings/provenance** — 3 limitations; mode=plan
- **PASS two-room-plan.png calibration provenance identity** — pixelWidth × metersPerPixel = 8.000000; declared width = 8
- **PASS two-room-plan-noisy.jpg wall count** — 8 detected; visible source has eight segments
- **PASS two-room-plan-noisy.jpg independently matched endpoints** — max endpoint deviation=0.018m, tolerance 0.15m (known 8×6m centerline plan)
- **PASS two-room-plan-noisy.jpg calibration/no furniture** — width=8.0m, objects=0, height=2.7m
- **PASS two-room-plan-noisy.jpg warnings/provenance** — 3 limitations; mode=plan
- **PASS two-room-plan-noisy.jpg calibration provenance identity** — pixelWidth × metersPerPixel = 8.000000; declared width = 8
- **PASS two-room-plan-skewed.png rejection** — Не найдено достаточно стен. Нужен контрастный план сверху без перспективы: тёмные горизонтальные и вертикальные стены на светлом фоне.
- **PASS blank.png rejection** — Не найдено достаточно стен. Нужен контрастный план сверху без перспективы: тёмные горизонтальные и вертикальные стены на светлом фоне.
- **PASS portable exact model roundtrip** — ZIP 4611 bytes; geometry, settings, file metadata equal
- **PASS SHA256 photo.png** — d03cc8399f49e25e8afa40f4dc5be3c11d41bf0bc67f5b20d5953350a01a63da
- **PASS SHA256 synthetic-video.mp4** — a36493ad568ea55bf54118d8129268bd95ab091cc5bbf98f55238cc2a4492bf5
- **PASS SHA256 custom-triangle.glb** — e60676f933a9476e6ed644b5c6b42f19499229f75ef7fd4bab09863549769117
- **PASS wall NaN rejected** — rejected
- **PASS wall Inf rejected** — rejected
- **PASS negative size rejected** — rejected
- **PASS point Inf rejected** — rejected
- **PASS duplicate object id rejected** — rejected
- **PASS missing asset rejected** — rejected
- **PASS nonobject opening rejected cleanly** — ValueError
- **PASS duplicate asset ids rejected cleanly** — ValueError
- **PASS missing source data rejected cleanly** — ValueError
- **PASS object missing color validation/export agreement** — validation rejects
- **PASS room missing name validation/export agreement** — validation rejects
- **PASS not ZIP rejected** — rejected
- **PASS bad base64 rejected** — rejected
- **PASS ZIP traversal rejected** — rejected without extraction
- **PASS SVG current-model door geometry** — original arcs=[[680.0, 545.0, 585.0, 545.0, 585.0, 545.0, 95.0, 95.0, 0.0, 0.0, 0.0, 680.0, 640.0], [745.0, 515.0, 745.0, 610.0, 745.0, 610.0, 95.0, 95.0, 0.0, 0.0, 0.0, 840.0, 515.0], [870.0, 655.0, 780.0, 655.0, 780.0, 655.0, 90.0, 90.0, 0.0, 0.0, 0.0, 870.0, 745.0], [600.0, 840.0, 600.0, 940.0, 600.0, 940.0, 100.0, 100.0, 0.0, 0.0, 0.0, 700.0, 840.0]]; translated arcs=[[680.0, 545.0, 585.0, 545.0, 585.0, 545.0, 95.0, 95.0, 0.0, 0.0, 0.0, 680.0, 640.0], [745.0, 515.0, 745.0, 610.0, 745.0, 610.0, 95.0, 95.0, 0.0, 0.0, 0.0, 840.0, 515.0], [870.0, 655.0, 780.0, 655.0, 780.0, 655.0, 90.0, 90.0, 0.0, 0.0, 0.0, 870.0, 745.0], [600.0, 840.0, 600.0, 940.0, 600.0, 940.0, 100.0, 100.0, 0.0, 0.0, 0.0, 700.0, 840.0]]
- **PASS SVG current-model wall dimensions** — modified extent must be 12.00m
- **PASS HTTP valid model** — 200 application/json; charset=utf-8
- **PASS HTTP malformed model** — 400 application/json; charset=utf-8
- **PASS HTTP nonfinite geometry** — 400 application/json; charset=utf-8
- **PASS HTTP deferred GPU honest unavailable** — 503 application/json; charset=utf-8
- **PASS HTTP archive roundtrip** — import 200; model equality
- **PASS HTTP actual SVG export** — 200; parsed XML; 18796 bytes

## Critic iteration history and limits

Initial output duplicated all four exterior walls (12 vs 8 segments) on both clean and noisy fixtures. Builder merged wall strips; the first independent rerun matched all eight known wall segments with maximum endpoint error 0.0646 m. A later junction/centreline correction reduced that error to 0.0180 m. Blank input and a 3-degree skew are explicitly rejected; recognition of arbitrary photographed plans is not established.

Initial SVG used hardcoded authored door coordinates. Anchored opening metadata now passes whole-model translation and changed wall extent checks. Missing room name/object color, null openings, duplicate asset IDs and missing source payload caused validation/export inconsistencies; builder fixed them and the independent malformed-model probes pass.

Archive checks use an original synthetic PNG fixture, an actual 0.6-second MP4 created by ffmpeg, and a valid generated triangle GLB. Exact bytes, metadata, modified geometry and settings survive both direct and HTTP archive roundtrips. This does not claim real apartment video reconstruction. GPU inference is explicitly deferred by the user and correctly returns unavailable; no external inference is exercised.

SVG XML and geometric consistency were checked, not a visual win against Floorplanner. Wall editing propagation in the browser, browser import state, walkthrough capture, real photograph robustness, and visual quality require separate integrated/visual review.
