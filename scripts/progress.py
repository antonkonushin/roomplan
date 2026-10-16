"""Append honest iteration evidence to the live page, preserving failed history."""
import argparse
import datetime
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--event', required=True)
parser.add_argument('--summary')
parser.add_argument('--round', type=int)
parser.add_argument('--gap', action='append')
parser.add_argument('--evidence', nargs=2, action='append', metavar=('LABEL', 'URL'))
args = parser.parse_args()
path = root / 'progress.json'
p = json.loads(path.read_text(encoding='utf-8-sig'))
stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%Y-%m-%d %H:%M МСК')
p['updated'] = stamp
p['history'].append({'time': stamp, 'text': args.event})
if args.summary: p['summary'] = args.summary
if args.round is not None: p['round'] = args.round
if args.gap is not None: p['gaps'] = args.gap
for label, url in args.evidence or []:
    if not any(e['url'] == url for e in p['evidence']):
        p['evidence'].append({'label': label, 'url': url})
temp = path.with_suffix('.tmp')
temp.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding='utf-8')
temp.replace(path)
print(stamp)
