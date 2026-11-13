#!/usr/bin/env python3
"""Copy the region data from a FindMeTunnel app checkout and rebuild index.json.

    python3 tools/update.py /path/to/FindMeTunnel <app-version>
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    app, version = sys.argv[1], sys.argv[2]
    data = os.path.join(app, 'FindMeTunnel', 'Data')
    sources = sorted(glob.glob(os.path.join(data, 'Regions', '*.json')))
    if not sources:
        sys.exit(f'no region files in {data}/Regions')

    out = os.path.join(HERE, 'regions')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    regions = []
    for path in sources:
        shutil.copy2(path, out)
        pack = json.load(open(path, encoding='utf-8'))
        kinds = {}
        for place in pack['places']:
            kinds[place['kind']] = kinds.get(place['kind'], 0) + 1
        regions.append({
            'id': pack['id'],
            'country': pack['country'],
            'name': pack['name'],
            'file': f"regions/{os.path.basename(path)}",
            'places': len(pack['places']),
            'kinds': dict(sorted(kinds.items())),
            'osm': pack.get('osm'),
            'generated': pack['generated'],
        })

    shutil.copy2(os.path.join(data, 'RegionBoundaries.json'),
                 os.path.join(HERE, 'boundaries.json'))

    index = {
        'app_version': version,
        'regions': len(regions),
        'places': sum(r['places'] for r in regions),
        'items': regions,
    }
    with open(os.path.join(HERE, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f"{index['regions']} regions, {index['places']} places, app {version}")


if __name__ == '__main__':
    main()
