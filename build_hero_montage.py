"""Make a continuous muted hero reel from supplied campaign films.

Each campaign gets five seconds, with a short overlap between excerpts. The
original ten-second title film begins the reel. Run after import_videos.py.
"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'dist' / 'assets'
campaigns = [x for x in json.loads((ROOT / 'video-imports.json').read_text())
             if x['category'] == 'campaign']
sources = [ASSETS / 'jhg-title-ten-seconds.mp4'] + [ROOT / 'dist' / x['video'].lstrip('/') for x in campaigns]
assert all(p.exists() for p in sources), 'Import the full-length campaign videos first.'

overlap = .45
durations = [10.0] + [5.0] * len(campaigns)
command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y']
for index, (path, seconds) in enumerate(zip(sources, durations)):
    if index:
        minutes, seconds_left = map(int, campaigns[index-1]['duration'].split(':'))
        total = 60 * minutes + seconds_left
        # Representative footage usually begins after the opening slate.
        start = min(total * .18, max(0, total - seconds - 1))
        command += ['-ss', f'{start:.2f}']
    command += ['-t', str(seconds), '-i', str(path)]

parts = []
for i in range(len(sources)):
    parts.append(f'[{i}:v]fps=24,scale=1280:720:force_original_aspect_ratio=increase,'
                 f'crop=1280:720,setsar=1,format=yuv420p,setpts=PTS-STARTPTS[v{i}]')
previous = 'v0'
elapsed = durations[0]
for i in range(1, len(sources)):
    output = f'm{i}'
    parts.append(f'[{previous}][v{i}]xfade=transition=fade:duration={overlap}:'
                 f'offset={elapsed-overlap:.2f}[{output}]')
    elapsed += durations[i]-overlap
    previous = output

target = ASSETS / 'jhg-campaign-montage.mp4'
with tempfile.NamedTemporaryFile(mode='w', suffix='.filter', delete=False) as script:
    script.write(';'.join(parts))
try:
    command += ['-filter_complex_script', script.name, '-map', f'[{previous}]',
                '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '28',
                '-maxrate', '1700k', '-bufsize', '3400k', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', str(target.with_suffix('.encoding.mp4'))]
    subprocess.run(command, check=True)
    target.with_suffix('.encoding.mp4').replace(target)
    print(f'Hero montage: {len(campaigns)} campaign clips; {elapsed:.1f}s; {target.stat().st_size:,} bytes')
finally:
    Path(script.name).unlink()
