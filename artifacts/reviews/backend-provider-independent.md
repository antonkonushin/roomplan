# Independent local object provider contract review

21/21 probes pass. Synthetic contract fixture only. No model weights, GPU inference, external endpoint, or app server on port 8765 was used.

- **PASS fixture GLB structurally valid** — 988 bytes; SHA256 e79fe7558c2f8ccaa71efb33518042ab8f76a79ed28e240c7552f331cb2de282
- **PASS actual API successful local provider** — HTTP 200; ephemeral app/provider ports
- **PASS first image forwarded exactly** — single-image seam sends first image only
- **PASS all originals preserved exactly** — both PNG bytes and metadata retained
- **PASS returned GLB preserved exactly** — e79fe7558c2f8ccaa71efb33518042ab8f76a79ed28e240c7552f331cb2de282
- **PASS asset bound to custom object** — custom asset id reference; scale/first-image limitations present
- **PASS provider result portable ZIP roundtrip** — actual HTTP ZIP and import; sources, GLB, object metadata equal
- **PASS reject provider http-failure** — HTTP 503; no geometry fallback expected
- **PASS reject provider wrong-mime** — HTTP 503; no geometry fallback expected
- **PASS reject provider invalid-base64** — HTTP 503; no geometry fallback expected
- **PASS reject provider invalid-magic** — HTTP 503; no geometry fallback expected
- **PASS reject provider missing-asset** — HTTP 503; no geometry fallback expected
- **PASS reject provider truncated-glb** — HTTP 503; no geometry fallback expected
- **PASS reject provider wrong-glb-version** — HTTP 503; no geometry fallback expected
- **PASS reject provider wrong-glb-length** — HTTP 503; no geometry fallback expected
- **PASS reject provider invalid-glb-json** — HTTP 503; no geometry fallback expected
- **PASS wrapper health disclaims inference** — ready-to-run is not inference verification
- **PASS real wrapper + fixture CLI + real API success** — HTTP 200; exact fixture GLB, not model output
- **PASS wrapper official CLI shape and image conversion** — {"size": [80, 64], "mode": "RGBA", "pixel": [255, 0, 0, 255], "texture": "1024"}
- **PASS wrapper rejects truncated GLB directly** — HTTP 503; invalid upstream output
- **PASS wrapper process failure propagated** — HTTP 503; no asset returned

The real Python app route and real sf3d_service wrapper were exercised on temporary loopback ports. The fake upstream run.py only copied a pre-existing valid synthetic GLB into the documented output path. This proves request/CLI/response and source/asset persistence contracts, not SF3D installation, model inference, shape quality, licensing, GPU performance, or browser rendering. Actual inference remains deferred.

## Critic iteration and final validation

Initial actual HTTP execution accepted the invalid four-byte payload `glTF` as a successful reconstructed asset. The critic reported this to the builder. Shared structural GLB validation was added to both the app adapter and service wrapper. The final independent rerun at 08:16 on 2026-10-16 rejected truncated content, wrong GLB version, inconsistent declared length, invalid JSON chunks, invalid magic/base64/MIME, and provider failures with 503 JSON and no substituted geometry.

The valid 988-byte synthetic GLB still passes both paths without byte changes, together with both original PNG sources and their metadata through actual HTTP portable ZIP export/import. The full repository regression suite was independently rerun after the fix: **29 tests passed, none skipped**. These are integration and failure-path findings, not evidence of actual model inference.
