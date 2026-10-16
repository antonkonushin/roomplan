# Research overlays, schema v1

Research layers display imported observations or hypotheses. They are separate from the built-in `pointCloud` reconstruction output and from CG camera route helpers. Importing a layer performs no reconstruction or inference.

The optional `project.researchLayers` array contains versioned layers. A portable import file uses this envelope:

```json
{
  "version": 1,
  "researchLayers": [
    {
      "version": 1,
      "id": "wall-hypothesis-01",
      "name": "Wall hypothesis",
      "kind": "lines",
      "visible": true,
      "units": "m",
      "coordinateFrame": "project-x-y-z",
      "positions": [[1, 0.1, 2], [3, 0.1, 2], [3, 2, 2]],
      "segments": [[0, 1], [1, 2]],
      "color": "#126fd6",
      "sourceIds": [],
      "assetIds": [],
      "provenance": {"method": "manual-hypothesis", "isSynthetic": true}
    }
  ]
}
```

Coordinates are metres in the project's coordinate frame: x and z are horizontal, y points upward. No automatic axis flip, scale inference, camera transform, or registration occurs. Convert centimetres, pixels, camera-local or world coordinates explicitly before importing; preserve the conversion method and original units in `provenance`.

`kind` is `points` or `lines`. Points use every position. Lines use explicit zero-based `segments` index pairs; there is no implicit polyline connectivity. Unknown kinds or versions are rejected rather than silently dropped. Future renderers should introduce a documented version or kind and corresponding validator.

All shown fields are required except `segments`, which is required and nonempty for lines and omitted or empty for points. IDs must be unique within `researchLayers`, nonempty, and at most 100 characters. Names have 1–200 characters; color is a six-digit hex value. Every coordinate is finite and within ±1000 m. Each layer has 1–100000 positions and at most 100000 segments. Project totals are limited to 64 layers, 200000 positions, and 200000 segments. Segment endpoints are distinct integer indices. `visible` is a boolean, retained independently per layer. `project.layers.research` is the master visibility switch and does not overwrite individual settings.

`sourceIds` and `assetIds` contain unique IDs resolving to the project's `sources` and `assets` arrays respectively. Empty references are valid for authored data. `provenance` is a JSON object retained without renaming or removing extension fields. Record method/version, synthetic versus measured status, calibration, and limitations when known; unknown evidence is not inferred.

## Import and persistence contract

1. Read the original JSON bytes; validate the envelope version and layers.
2. Add those exact original bytes to `project.assets` as an `application/json` asset with a unique ID. Do not reserialize the input to represent the original.
3. Append that new asset ID to each imported layer's `assetIds`. Resolve any other references to existing project assets/sources. Reject duplicate layer IDs or require an explicit ID remapping.
4. Submit the candidate project to `/api/validate` before changing the active project. Only install the validated result. Validation failures leave the active project untouched.
5. Save with the ordinary ZIP API: parsed geometry and flags remain in `project.json`; original bytes are stored under `assets/`. Load restores both. Old projects without `researchLayers` remain valid.

The shared renderer exports `buildResearchLayers(project)` from `web/research.js`. It returns a visible `THREE.Group` named `research-layers`, with one child group per layer. Child names are `research:<id>` and `userData.researchLayerId` is the stable data ID across rebuilds. Three.js runtime numeric IDs and UUIDs are not persistence IDs. Child visibility comes from the layer; attach the root under the scene's research master group. Dispose geometries and materials with the normal scene teardown. The renderer creates `THREE.Points` and indexed `THREE.LineSegments`, with no camera helpers or inferred geometry.

Run `python scripts/create_asset_fixture.py` to regenerate `artifacts/fixtures/research-layers.json` and the portable `asset-project.zip`. The fixture contains two explicitly synthetic, independently visible layers. Its original JSON is preserved byte-for-byte as an asset; the fixture is not evidence of recovered geometry from photos or video.
