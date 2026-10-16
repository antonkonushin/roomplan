# Browser acceptance checkpoint — 2026-10-16

Actual in-app browser interactions, not a simulated DOM. Local server http://127.0.0.1:8765.

- Plan import: two-room-plan.png, 8 m centreline calibration and 2.7 m ceiling. Eight wall segments, no furniture. Original source visible. Synthetic input only; arbitrary photographed plan accuracy is not established.
- Wall lifecycle failure found after saving: validation replaced the live project while inspector closures retained previous objects. Neighbour walls moved but selected wall remained unchanged. Preserved downloaded ZIP: round3-wall-edit-failure.zip. Builder removed live-project replacement from Save.
- Retest: open original project, select top wall, Save, type length9 and height3.1 using keyboard, Save. UI reads9.00/3.10; actual downloaded round4-edited-project.zip contains w1 length9.0 and height3.1. Neighbor wall and room extent follow. Screenshot round4-wall-edit-2d.jpg. Revised2D wall contrast is readable.
- Video input: synthetic-walkthrough.mp4 imported through Video tab, explicit demo warning. Furnished demo + point cloud appears. Cloud, object boxes and camera layers enabled; 2D view selected. Saved round3-video-project.zip, replaced scene with demo, reopened saved ZIP. Title, source filename, 2D mode and allthree layer toggles restored. Archive source bytes exactly equal input MP4.
- Multi-view input: two app-generated PNGs selected through multiple-file chooser. Explicit demo scene, both originals listed, deterministic-demo-stub-v1 provenance. Screenshot round3-multiview-import.jpg. This is not real reconstruction.
- Object reconstruction: uploaded generated PNG and attempted local inference with no service. Explicit unavailable/SF3D-not-run message, source retained. Screenshot round3-gpu-unavailable.jpg. Actual GPU inference remains user-deferred.
- Video export: actual downloaded round3-orbit.webm, FFprobe confirms VP9,1280x720,15fps,45 decoded frames,3.000seconds. Extracted chronological frames show camera movement. However full walls from prior interior mode occluded overview; builder now enforces cutaway for overview. Second interior path and final playback still require retest.
- PNG/SVG actual browser downloads retained as round3/round4 exports. Independent visual report remains FAIL. No photorealistic win claimed.

Remaining integrated checks: final interior walkthrough, updated overview composition, customGLB in actual viewer, final project export/reopen after asset handling, visual reference wins.
