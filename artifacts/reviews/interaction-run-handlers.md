# Preview/record handler regression — independent executed evidence

**8/8 checks PASS.** Run: `node scripts/critic_interaction_run_handlers.mjs`. Timestamp and source hashes: [interaction-run-handlers.json](interaction-run-handlers.json).

This test executes the actual production `showWalkthrough()` registration, `#preview-walk`/`#record-walk` callbacks, `lockRoute()` and the actual production `RoomScene.walkthrough()` loop. It parses the static HTML and dynamic modal/path markup into minimal individual DOM elements. `querySelector()` returns one element, with **no `.forEach` method**; `querySelectorAll()` returns the matching collection. Four actual generated remove-point buttons are present during the check.

Results:

- Preview completes, invokes progress updates through 100%, and restores every disabled route control and remove-point button. The virtual timer produces 189 render-loop iterations for the requested 3 seconds.
- Record renders exactly **45 frames**, sends **15 fps / 1280×720** to the encoder boundary, reports progress through 100%, and invokes one WebM download.
- Every rendered frame observes all route controls and remove-point buttons locked. The request to the encoder also observes them locked.
- Injected encoder failure reaches the user-visible status, restores controls, leaves `recording=false`, and creates no extra download.
- “Точки в сцене” sets `layers.cameras=true`; the initially false `layers.research` remains false.

## Negative control for the exact browser failure

The test runs a second isolated VM with **only** the original selector mistake restored in memory: `$$('[data-remove-path]').forEach(...)` becomes `$('[data-remove-path]').forEach(...)`. No production file is modified.

The negative control reproduces `$(...).forEach is not a function`, produces **zero frames**, and leaves route controls disabled. Therefore this DOM substitute does not hide the original singleton-versus-collection bug. The regression would fail if that mistake returned.

## Limits

GPU rendering, elapsed clock time, encoded response bytes and the download sink are substituted. The response blob is explicitly dummy data, **not a playable video**; no media file is delivered from this test. This verifies callback sequencing, progress, locking, cleanup and download invocation. Real browser performance, actual encoding and playback belong to the lead's separate end-to-end evidence. No catalog construction or geometry tests were repeated for this focused check.
