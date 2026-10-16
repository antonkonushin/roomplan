import base64
import io
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
from roomplan.glb import validate_glb
from roomplan.providers import reconstruct_object, ProviderUnavailable

FIXTURE = Path(__file__).resolve().parents[1] / 'artifacts/fixtures/wide-test-object.glb'


def repack(document, binary):
    text=json.dumps(document,separators=(',',':')).encode();text+=b' '*((-len(text))%4)
    return struct.pack('<III',0x46546c67,2,28+len(text)+len(binary))+struct.pack('<II',len(text),0x4e4f534a)+text+struct.pack('<II',len(binary),0x004e4942)+binary


class GLBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.valid=FIXTURE.read_bytes()

    def bad_variants(self):
        data=self.valid
        return [b'glTF',data[:4]+struct.pack('<I',3)+data[8:],data[:8]+struct.pack('<I',len(data)+16)+data[12:],
                data[:20]+b'!'+data[21:],data[:12]+struct.pack('<I',len(data)*2)+data[16:],
                data[:12]+struct.pack('<I',5)+data[16:],data[:16]+struct.pack('<I',0x004e4942)+data[20:]]

    def test_valid_fixture_preserves_bytes_and_contains_mesh(self):
        before=self.valid[:];doc=validate_glb(self.valid)
        self.assertTrue(doc['meshes']);self.assertEqual(before,self.valid)

    def test_header_chunk_and_json_corruption_rejected(self):
        for data in self.bad_variants():
            with self.subTest(size=len(data)),self.assertRaises(ValueError): validate_glb(data)

    def test_embedded_buffer_and_accessor_bounds_rejected(self):
        json_length=struct.unpack_from('<I',self.valid,12)[0]
        original=json.loads(self.valid[20:20+json_length]);binary=self.valid[28+json_length:]
        for field in ['buffer','view','accessor','reference','empty','sparse']:
            doc=json.loads(json.dumps(original))
            if field=='buffer': doc['buffers'][0]['byteLength']=len(binary)+4
            if field=='view': doc['bufferViews'][0]['byteLength']=len(binary)+4
            if field=='accessor': doc['accessors'][0]['count']+=1
            if field=='reference': doc['meshes'][0]['primitives'][0]['attributes']['POSITION']=999
            if field=='empty': doc['meshes']=[]
            if field=='sparse':
                doc['accessors'][0]['sparse']={'count':999,'indices':{'bufferView':0,'componentType':5123},'values':{'bufferView':0}}
            with self.subTest(field=field),self.assertRaises(ValueError): validate_glb(repack(doc,binary))

    def test_provider_rejects_malformed_mesh_instead_of_success(self):
        payload={'name':'Synthetic contract','files':[{'name':'photo.png','mime':'image/png','data':'YWJj'}]}
        for data in self.bad_variants():
            response=json.dumps({'asset':{'name':'mesh.glb','mime':'model/gltf-binary','data':base64.b64encode(data).decode()}}).encode()
            with patch.dict('os.environ',{'ROOMPLAN_RECONSTRUCTION_URL':'http://127.0.0.1:8877/reconstruct'}),patch('urllib.request.urlopen',return_value=io.BytesIO(response)):
                with self.assertRaises(ProviderUnavailable): reconstruct_object(payload)


if __name__=='__main__': unittest.main()
