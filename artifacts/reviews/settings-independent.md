# Independent saved-settings validation

```json
{
  "result": "PASS",
  "scope": "Independent real HTTP requests to fresh ephemeral ThreadingHTTPServer using production Handler; no mocks, no builder test counts, no browser rendering claim.",
  "checks": 43,
  "sourceSHA256": {
    "roomplan/model.py": "4052fd9508d8ec64ceeb571fa116764dc9d7e197918dd6183d47f85af5f80b80",
    "server.py": "ed84d472ef451605a41788b5af75066ec7178be62d557a0763a2da22e0d6f9fd",
    "roomplan/storage.py": "9c51d1868cbdbf4a2850ff54926dde12cd6bb9c6b6745cd1ca8bbd8347b9793e"
  },
  "results": [
    {
      "case": "camera missing target",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.camera.target: требуется 3 координат"
    },
    {
      "case": "camera missing target",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.target: требуется 3 координат"
    },
    {
      "case": "camera missing target",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.target: требуется 3 координат"
    },
    {
      "case": "ortho missing position",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.orthoCamera.position: требуется 3 координат"
    },
    {
      "case": "ortho missing position",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.orthoCamera.position: требуется 3 координат"
    },
    {
      "case": "ortho missing position",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.orthoCamera.position: требуется 3 координат"
    },
    {
      "case": "camera numeric strings",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera numeric strings",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera numeric strings",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera boolean",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera boolean",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera boolean",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.camera.position: ожидается конечное число в диапазоне -1000…1000"
    },
    {
      "case": "camera NaN",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "Неконечное число в проекте"
    },
    {
      "case": "camera NaN",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "Неконечное число в проекте"
    },
    {
      "case": "camera NaN",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "Неконечное число в проекте"
    },
    {
      "case": "walkpoint missing target",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.walkPath[0].target: требуется 3 координат"
    },
    {
      "case": "walkpoint missing target",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.walkPath[0].target: требуется 3 координат"
    },
    {
      "case": "walkpoint missing target",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.walkPath[0].target: требуется 3 координат"
    },
    {
      "case": "settings list",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "settings list",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "settings list",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "null settings",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "null settings",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "null settings",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings: ожидается объект"
    },
    {
      "case": "invalid FOV",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.cameraFov: угол должен быть больше 0 и меньше 180"
    },
    {
      "case": "invalid FOV",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.cameraFov: угол должен быть больше 0 и меньше 180"
    },
    {
      "case": "invalid FOV",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.cameraFov: угол должен быть больше 0 и меньше 180"
    },
    {
      "case": "zero zoom",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.orthoZoom: ожидается конечное число в диапазоне 1e-06…1000000.0"
    },
    {
      "case": "zero zoom",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.orthoZoom: ожидается конечное число в диапазоне 1e-06…1000000.0"
    },
    {
      "case": "zero zoom",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.orthoZoom: ожидается конечное число в диапазоне 1e-06…1000000.0"
    },
    {
      "case": "string flag",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.cutaway: ожидается логическое значение"
    },
    {
      "case": "string flag",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.cutaway: ожидается логическое значение"
    },
    {
      "case": "string flag",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.cutaway: ожидается логическое значение"
    },
    {
      "case": "unknown view",
      "endpoint": "/api/validate",
      "status": 400,
      "pass": true,
      "error": "settings.view: неизвестное значение"
    },
    {
      "case": "unknown view",
      "endpoint": "/api/export/project",
      "status": 400,
      "pass": true,
      "error": "settings.view: неизвестное значение"
    },
    {
      "case": "unknown view",
      "endpoint": "/api/import/project",
      "status": 400,
      "pass": true,
      "error": "settings.view: неизвестное значение"
    },
    {
      "case": "2d nondefault settings validate exact preservation",
      "status": 200,
      "pass": true
    },
    {
      "case": "2d HTTP ZIP roundtrip exact project/settings/extension preservation",
      "exportStatus": 200,
      "importStatus": 200,
      "pass": true
    },
    {
      "case": "3d nondefault settings validate exact preservation",
      "status": 200,
      "pass": true
    },
    {
      "case": "3d HTTP ZIP roundtrip exact project/settings/extension preservation",
      "exportStatus": 200,
      "importStatus": 200,
      "pass": true
    },
    {
      "case": "legacy optional settings absent",
      "status": 200,
      "pass": true
    },
    {
      "case": "legacy optional settings {}",
      "status": 200,
      "pass": true
    },
    {
      "case": "legacy optional settings {'futureOnly': [1, 2, 3]}",
      "status": 200,
      "pass": true
    }
  ]
}
```

## Narrow production-handler recheck

Existing script executed against a fresh ephemeral server. In-memory changes only: root URL for data-module import, fetch URL redirected from port 8765, original report write suppressed to preserve previous evidence. No production code modifications.

Exit code: 0

```json
{
  "at": "2026-10-16T09:37:43.748Z",
  "scope": "Production JS callbacks, actual Three camera/group math and actual HTTP ZIP. Minimal DOM, no browser/render/picking claims.",
  "sourceSHA256": {
    "web/app.js": "a2de0feed386d186d3924e62e89bc01673b7b82953ccb854d4def8d922e815db",
    "web/editing.js": "d0e10fb6f5e127ec85db5b7ce869517de32cd8f35549f896ddddd6e0ef7497c8",
    "web/scene.js": "94a125cbd88037688ca59e3af44422aa4ae51c2f384a7073c25348ec8626a715",
    "roomplan/model.py": "4052fd9508d8ec64ceeb571fa116764dc9d7e197918dd6183d47f85af5f80b80"
  },
  "results": [
    {
      "name": "Reject invalid wall dimension 0=0",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "0",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 0=-1",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "-1",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 0=",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 0=abc",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "abc",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 0=Infinity",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "Infinity",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 0=0.005",
      "status": "PASS",
      "evidence": {
        "index": 0,
        "value": "0.005",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Длина: укажите значение от 0.01 до 30 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 1=0.05",
      "status": "PASS",
      "evidence": {
        "index": 1,
        "value": "0.05",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Высота: укажите значение от 0.1 до 10 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 1=12",
      "status": "PASS",
      "evidence": {
        "index": 1,
        "value": "12",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Высота: укажите значение от 0.1 до 10 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 2=0.005",
      "status": "PASS",
      "evidence": {
        "index": 2,
        "value": "0.005",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Толщина: укажите значение от 0.01 до 2 м."
      }
    },
    {
      "name": "Reject invalid wall dimension 2=3",
      "status": "PASS",
      "evidence": {
        "index": 2,
        "value": "3",
        "sameWalls": true,
        "historyDelta": 0,
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            10,
            0
          ],
          "height": 2.8,
          "thickness": 0.16
        },
        "toast": "Толщина: укажите значение от 0.01 до 2 м."
      }
    },
    {
      "name": "2d all master states actual handlers and ZIP reload",
      "status": "PASS",
      "evidence": {
        "expected": {
          "architecture": false,
          "furniture": false,
          "pointCloud": true,
          "boxes": true,
          "research": true,
          "cameras": true
        },
        "rendered": {
          "architecture": false,
          "furniture": false,
          "pointCloud": true,
          "boxes": true,
          "research": true,
          "cameras": true
        },
        "mode": "2d"
      }
    },
    {
      "name": "3d all master states actual handlers and ZIP reload",
      "status": "PASS",
      "evidence": {
        "expected": {
          "architecture": false,
          "furniture": false,
          "pointCloud": true,
          "boxes": true,
          "research": true,
          "cameras": true
        },
        "rendered": {
          "architecture": false,
          "furniture": false,
          "pointCloud": true,
          "boxes": true,
          "research": true,
          "cameras": true
        },
        "mode": "3d"
      }
    },
    {
      "name": "2d translated camera restored",
      "status": "PASS",
      "evidence": {
        "before": {
          "position": [
            7,
            25,
            4.25100000004197
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1.7
        },
        "after": {
          "position": [
            7,
            25,
            4.25100000004197
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1.7
        }
      }
    },
    {
      "name": "2d framing after switching away/back",
      "status": "OBSERVATION",
      "evidence": {
        "before": {
          "position": [
            7,
            25,
            4.25100000004197
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1.7
        },
        "after": {
          "position": [
            5,
            25,
            3.2510000000419703
          ],
          "target": [
            5,
            0,
            3.25
          ],
          "zoom": 1.7
        },
        "reset": true,
        "note": "setMode intentionally calls fit; retaining per-view framing is a UX limitation, not an explicit acceptance requirement."
      }
    },
    {
      "name": "3d translated camera restored",
      "status": "PASS",
      "evidence": {
        "before": {
          "position": [
            15.84,
            11.559999999999999,
            15.809999999999997
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1
        },
        "after": {
          "position": [
            15.84,
            11.559999999999999,
            15.809999999999997
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1
        }
      }
    },
    {
      "name": "3d framing after switching away/back",
      "status": "OBSERVATION",
      "evidence": {
        "before": {
          "position": [
            15.84,
            11.559999999999999,
            15.809999999999997
          ],
          "target": [
            7,
            0,
            4.25
          ],
          "zoom": 1
        },
        "after": {
          "position": [
            13.84,
            11.559999999999999,
            14.809999999999997
          ],
          "target": [
            5,
            0,
            3.25
          ],
          "zoom": 1
        },
        "reset": true,
        "note": "setMode intentionally calls fit; retaining per-view framing is a UX limitation, not an explicit acceptance requirement."
      }
    },
    {
      "name": "Fresh model loads actual corrected-wall ZIP",
      "status": "PASS",
      "evidence": {
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            9,
            0
          ],
          "height": 3.1,
          "thickness": 0.1398
        }
      }
    },
    {
      "name": "Corrected-wall ZIP remains editable",
      "status": "PASS",
      "evidence": {
        "wall": {
          "id": "w1",
          "a": [
            0,
            0
          ],
          "b": [
            9.5,
            0
          ],
          "height": 3.2,
          "thickness": 0.1398
        }
      }
    },
    {
      "name": "Malformed camera is rejected before replacing working project",
      "status": "PASS",
      "evidence": {
        "apiAccepted": false,
        "workingProjectRetained": true,
        "currentName": "Квартира · Тёплый минимализм"
      }
    }
  ]
}

```
