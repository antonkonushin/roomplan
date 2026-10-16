# Independent backend re-audit — 2026-10-15 23:55

Current running application on `http://127.0.0.1:8765` was tested after restart. No production code was edited by the critic.

- **38/38 independent backend probes pass** (`scripts/critic_backend.py --url http://127.0.0.1:8765`). Full evidence and exact source/asset hashes: `backend-independent.md`.
- **11/11 independent video API probes pass** (`scripts/critic_backend_video.py`). Full encoded-stream and decoded-frame evidence: `backend-video-independent.md`.
- **19/19 repository unit/regression tests pass**, independently rerun with `python -m unittest discover -s tests -v`. No skipped tests in this run. Windows localhost and temporary-file execution used approved elevation.

Recognition now matches all eight known wall segments in the independently supplied clean and noisy synthetic fixtures with maximum endpoint deviation **0.0180 m**, improved from the prior 0.0646 m. Requested width remains exactly 8 m; topology regression verifies shared outer corners and preserved door gaps. Blank and 3-degree-skew images are explicitly rejected. This establishes the supported synthetic baseline, not arbitrary photographed-plan accuracy.

Two actual new defects were found, reported to the lead, fixed, and retested:

1. A JPEG truncated to its first 650 bytes retained valid headers and passed Pillow `verify()`, so the HTTP video API accepted malformed frames and returned 200. Explicit image decoding now rejects this input with 400 JSON. The independent test remains in the video critic script, and the lead added a regression test.
2. After centreline calibration, `pixelWidth` retained the raw stroke envelope while `metersPerPixel` referred to the joined wall centreline envelope. Their product disagreed with `widthMeters`. Raw width is now separate metadata and the calibrated identity holds for clean/noisy fixtures: `pixelWidth × metersPerPixel = 8.000000`.

The actual video HTTP response was independently probed and decoded: VP9, 160×96, 24 frames at 12 fps, 2.000 seconds, correctly ordered 8 red → 8 green → 8 blue frames. Invalid fps, odd dimensions, zero/excess frame counts, malformed base64, dimension mismatch, PNG instead of JPEG, and truncated JPEG all return 400 JSON.

Exported SVG still passes XML parsing, changed extent, and translated opening geometry checks. The new label search uses conservative furniture bounds but falls back in congested rooms; its visual benefit needs the separate visual critic. Video checks establish encoder/timeline fidelity only. They do not establish browser camera path geometry, collision avoidance, rendered quality, or completion of the deferred GPU integration. No visual superiority claim is made by this review.
