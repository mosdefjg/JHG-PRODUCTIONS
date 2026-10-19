"""Create full length, seekable web MP4s and posters from supplied masters.

Usage: python import_videos.py /absolute/path/to/masters
The uploaded masters are kept outside the published website.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / 'video-imports.json').read_text())
DEST = ROOT / 'dist/assets/media'
DEST.mkdir(parents=True, exist_ok=True)
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'video-masters'


def run(item):
    master = SOURCE / item['source']
    if not master.exists():
        raise FileNotFoundError(master)
    slug = item['slug']
    target = DEST / f'{slug}.mp4'
    poster = DEST / f'{slug}.webp'
    m, s = map(int, item['duration'].split(':'))
    duration = 60 * m + s
    if not target.exists() or target.stat().st_size < 10000:
        temp = DEST / f'{slug}.encoding.mp4'
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(master),
            '-map', '0:v:0', '-map', '0:a:0?',
            '-vf', 'scale=w=1280:h=-2:force_original_aspect_ratio=decrease:flags=lanczos,scale=trunc(iw/2)*2:trunc(ih/2)*2',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '30',
            '-maxrate', '1200k', '-bufsize', '2400k', '-pix_fmt', 'yuv420p',
            '-threads', '2', '-c:a', 'aac', '-b:a', '72k',
            '-movflags', '+faststart', str(temp)], check=True)
        temp.replace(target)
    if not poster.exists():
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-ss', str(min(duration * .18, 35)), '-i', str(master),
            '-frames:v', '1', '-vf', 'scale=w=960:h=-2:force_original_aspect_ratio=decrease',
            '-quality', '78', str(poster)], check=True)
    return slug, duration, target.stat().st_size


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('VIDEO_IMPORT_WORKERS', '4'))) as pool:
        for result in concurrent.futures.as_completed([pool.submit(run, x) for x in MANIFEST]):
            print(*result.result(), flush=True)
