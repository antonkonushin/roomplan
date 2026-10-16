# Independent raster scope verification — 2026-10-16

Reviewer: fresh subagent, independent from implementation, not blind. Scope: the active 2026-10-16 amendment in docs/quality-bar.md and docs/acceptance.md; ordinary Three.js rendering/walkthroughs, no photorealism or ray-tracing gate. This is a focused regression check, not a repeat of all F01–F15 scenarios.

## Direct observations

- Started a fresh browser tab at http://127.0.0.1:8765 after the lead restarted the interrupted server. Initial connection refusal was a stopped test server, not a product defect.
- Opened Export. Actual menu contains furnished SVG plan, current-camera PNG, interior viewpoint then PNG, and WebM walkthrough. Physical/path-tracing export is absent. Evidence: raster-scope-menu.png.
- Clicked current-camera PNG. The app reported successful download. Opened the actual downloaded file independently with the image viewer, then preserved it as raster-scope-dollhouse.png. Native size 2036 x 1364; SHA-256 902102124948E51A4E58D4E8A3A5981DADDAC676FFDEE1284CB28888E50B04C7. This is the app export, not a screenshot or substitute render.
- The PNG is populated and legible: joined walls and floor, supported recognizable sofa/chair/table/kitchen/bed/bath fixtures, contact shadows, restrained surfaces, generous whole-apartment framing, no editor decoration or missing/black canvas. No critical visible geometry or camera clipping regression in this output.
- Opened Video walkthrough from that same menu. Overview route had four points; Interior route switched to two points at y=1.6 m, turned off wall cutaway, and displayed ordinary-CG wording. Preview and Record WebM controls remained enabled; custom-view addition, scene path points, duration and overview choice remained present. Evidence: raster-scope-walkthrough.png. Did not rerender previously verified videos gratuitously; this check does not independently re-establish F11 playback/duration.
- Closed the dialog and inspected the actual interior camera: complete ceiling/walls/window; furniture and floor remain readable with contact depth and supported legs, no blank canvas or near-plane slicing. Evidence: raster-scope-interior-screen.png. This is a screenshot of current interior UI, not a fresh interior exported PNG.
- Static inspection of web/index.html, web/app.js and web/scene.js found only ordinary Three.js import map and raster/postprocessing imports. No physical-render entry, path-tracer import or windowLights/RectAreaLight reference in these three files. This is a source-entry check, not a runtime network-resource trace.

## Verdict and biggest remaining gap

PASS for this scope-change regression check: ordinary PNG export and interior route controls remain working after physical rendering removal. No photorealistic parity or Floorplanner superiority claim is made; this is not a complete independent acceptance of every visual class.

The largest visible remaining presentation limitation in the fresh output is the default dollhouse camera's foreground tall dark wardrobe: it obscures most of the TV/cabinet and the central circulation area. This is ordinary scene occlusion, not failed geometry, and does not by itself block the revised ordinary-CG scope. Reproduction: clean demo → Export → Current viewpoint PNG. Recommended optional improvement: provide a second dollhouse preset from the opposite side or a selective tall-furniture cutaway for listing views. Retest: not implemented/not retested in this focused review. No implementation changes made.
