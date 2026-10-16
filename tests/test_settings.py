"""Saved viewer settings must be safe before an import replaces the open model."""
import base64
import copy
import io
import json
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from http.server import ThreadingHTTPServer

from roomplan.model import demo_project, validate_project
from roomplan.storage import load_project, save_project
from server import Handler


def camera_point():
    return {'position': [14, 15, 18], 'target': [4, 0, 3]}


def unchecked_archive(project):
    """Emulate an externally authored ZIP, bypassing the export validator."""
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr('project.json', json.dumps(project))
    return base64.b64encode(stream.getvalue()).decode()


class SettingsTests(unittest.TestCase):
    def test_legacy_optional_and_unknown_settings_are_preserved(self):
        for settings in [None, {}, {'view': '2d'}, {'extension': {'revision': 2}}]:
            with self.subTest(settings=settings):
                project = demo_project()
                if settings is not None:
                    project['settings'] = settings
                original = copy.deepcopy(project)
                validated, _ = validate_project(project)
                self.assertEqual(validated, original)
                restored, _ = load_project(base64.b64encode(save_project(project)).decode())
                self.assertEqual(restored, original)
                self.assertEqual(project, original)

    def test_complete_saved_view_and_draft_routes_roundtrip(self):
        for view in ['2d', '3d']:
            for route in [[], [camera_point()], [camera_point(), camera_point()]]:
                with self.subTest(view=view, points=len(route)):
                    project = demo_project()
                    project['settings'] = {
                        'view': view, 'camera': camera_point(),
                        'orthoCamera': {'position': [4, 25, 3.001], 'target': [4, 0, 3]},
                        'cameraFov': 58, 'orthoZoom': 1.7, 'light': 1.1,
                        'cutaway': False, 'dimensions': True, 'roomLabels': False,
                        'walkPath': route, 'walkPathMode': 'custom',
                        'extension': {'futureSetting': True},
                    }
                    restored, _ = load_project(base64.b64encode(save_project(project)).decode())
                    self.assertEqual(restored, project)

    def test_invalid_known_settings_rejected(self):
        cases = [None, [], 'settings']
        for field in ['camera', 'orthoCamera']:
            for point in [None, [], {}, {'position': [1, 2, 3]}, {'target': [0, 0, 0]}]:
                cases.append({field: point})
            for key in ['position', 'target']:
                for vector in [[1, 2], [1, 2, 3, 4], '123', [1, '2', 3],
                               [1, True, 3], [1, None, 3], [1001, 2, 3],
                               [float('nan'), 2, 3], [1, float('inf'), 3]]:
                    point = camera_point()
                    point[key] = vector
                    cases.append({field: point})
        for field in ['cutaway', 'dimensions', 'roomLabels']:
            cases.extend({field: value} for value in [None, 0, 1, 'false', [], {}])
        for field in ['view', 'walkPathMode']:
            cases.extend({field: value} for value in [None, '', 'unexpected', 1, [], {}])
        for field in ['cameraFov', 'orthoZoom', 'light']:
            cases.extend({field: value} for value in [None, True, '1', 0, -1, float('inf')])
        cases.extend([{'cameraFov': 180}, {'cameraFov': 181},
                      {'orthoZoom': 1e-7}, {'orthoZoom': 1e7}, {'light': 1001}])
        cases.extend({'walkPath': route} for route in [None, {}, 'route', [None],
                     [{'position': [1, 2, 3]}],
                     [{'position': [1, 2, 3], 'target': [1, '2', 3]}],
                     [camera_point()] * 2001])
        for settings in cases:
            with self.subTest(settings=str(settings)[:200]):
                project = demo_project()
                project['settings'] = settings
                with self.assertRaises(ValueError):
                    validate_project(project)


class SettingsAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_incomplete_camera_rejected_by_validate_export_and_zip_import(self):
        project = demo_project()
        project['settings'] = {'camera': {'position': [1, 2, 3]}}
        for endpoint, payload in [
            ('/api/validate', {'project': project}),
            ('/api/export/project', {'project': project}),
            ('/api/import/project', {'data': unchecked_archive(project)}),
        ]:
            with self.subTest(endpoint=endpoint):
                request = urllib.request.Request(self.url + endpoint,
                    data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(request)
                self.assertEqual(error.exception.code, 400)
                response = json.load(error.exception)
                self.assertIn('settings.camera.target', response['error'])
                self.assertNotIn('project', response)


if __name__ == '__main__':
    unittest.main()
