"""Restore large static assets from the public Sites preview for a GitHub build.

The checked-in hosted-assets.json pins every download by SHA-256. The original
site remains a staging source until the owner chooses a permanent media host.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGIN = 'https://jhg-productions.john-h-guess.chatgpt.site'
MANIFEST = ROOT / 'hosted-assets.json'


def checksum(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


if __name__ == '__main__':
    if '--write-manifest' in sys.argv:
        files = (p for p in (ROOT / 'dist/assets').rglob('*') if p.is_file()
                 and (p.stat().st_size > 500_000 or '/media/' in str(p)))
        data = [{'path': str(p.relative_to(ROOT)), 'sha256': checksum(p), 'bytes': p.stat().st_size}
                for p in sorted(files)]
        MANIFEST.write_text(json.dumps(data, indent=2) + '\n')
        print(f'Pinned {len(data)} large assets for repository deployment.')
        sys.exit(0)

    data = json.loads(MANIFEST.read_text())
    for asset in data:
        relative = Path(asset['path'])
        if relative.parts[:2] != ('dist', 'assets') or '..' in relative.parts:
            raise ValueError(relative)
        target = ROOT / relative
        if target.exists() and checksum(target) == asset['sha256']:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + '.download')
        url = ORIGIN + '/' + str(relative.relative_to('dist'))
        urllib.request.urlretrieve(url, temporary)
        if checksum(temporary) != asset['sha256']:
            temporary.unlink()
            raise RuntimeError(f'Asset checksum mismatch: {relative}')
        temporary.replace(target)
        print(f'Downloaded {relative}')
