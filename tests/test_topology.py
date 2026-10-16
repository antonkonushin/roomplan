import base64
import unittest
from pathlib import Path
from roomplan.reconstruction import reconstruct


class ImportedTopologyTests(unittest.TestCase):
    def test_outer_corners_are_shared_and_door_gaps_remain(self):
        raw=Path('artifacts/fixtures/two-room-plan.png').read_bytes()
        p,_=reconstruct({'mode':'plan','files':[{'name':'plan.png','mime':'image/png','data':base64.b64encode(raw).decode()}],'widthMeters':8,'ceilingHeight':2.7})
        for corner in p['rooms'][0]['polygon']:
            self.assertGreaterEqual(sum(corner==wall[key] for wall in p['walls'] for key in ('a','b')),2)
        self.assertEqual(len(p['walls']),8)
        interior_vertical=[w for w in p['walls'] if 3<w['a'][0]<5 and w['a'][0]==w['b'][0]]
        self.assertEqual(len(interior_vertical),2)
        interior_vertical.sort(key=lambda w:w['a'][1])
        self.assertGreater(interior_vertical[1]['a'][1]-interior_vertical[0]['b'][1],.7)


if __name__=='__main__': unittest.main()
