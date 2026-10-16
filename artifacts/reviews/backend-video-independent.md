# Independent video API review

11/11 probes pass. Current app server on localhost:8765, 2026-10-15.

- **PASS actual video endpoint** — 200 video/webm; 1312 bytes
- **PASS encoded frame count size rate duration** — {"programs": [], "stream_groups": [], "streams": [{"codec_name": "vp9", "width": 160, "height": 96, "r_frame_rate": "12/1", "nb_read_frames": "24"}], "format": {"duration": "2.000000"}}
- **PASS decoded exact color timeline order** — [(225, 41, 42), (225, 41, 42), (225, 41, 42), (225, 41, 42), (225, 41, 42), (225, 41, 42), (225, 41, 42), (225, 41, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (43, 225, 42), (41, 41, 226), (41, 41, 226), (41, 41, 226), (41, 41, 226), (41, 41, 226), (41, 41, 226), (41, 41, 226), (41, 41, 226)]
- **PASS reject bool fps** — 400 application/json; charset=utf-8; bytes=89
- **PASS reject odd width** — 400 application/json; charset=utf-8; bytes=110
- **PASS reject zero frames** — 400 application/json; charset=utf-8; bytes=60
- **PASS reject too many frames** — 400 application/json; charset=utf-8; bytes=60
- **PASS reject bad base64** — 400 application/json; charset=utf-8; bytes=40
- **PASS reject wrong dimensions** — 400 application/json; charset=utf-8; bytes=123
- **PASS reject non JPEG** — 400 application/json; charset=utf-8; bytes=123
- **PASS reject truncated JPEG** — 400 application/json; charset=utf-8; bytes=65

This uses generated test frames, then probes and decodes the actual HTTP WebM response. It establishes encoding/timeline fidelity; it does not establish browser camera trajectory, absence of wall collisions, CG quality, or real apartment reconstruction.
