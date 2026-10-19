# JHG Productions

A cinematic, responsive eight-page portfolio for John H. Guess. The public Sites preview lives at https://jhg-productions.john-h-guess.chatgpt.site. The original Wix site remains separate.

## Pages and source

- Home, Work, Campaigns, AI & Animation, 3D Rendering, Services, About, and Contact are generated from `build_site.py` into `dist/`.
- `campaigns-source.json` and `specialties-source.json` describe previously listed work. `video-imports.json` lists the supplied video masters, editorial titles, groups, durations, and output paths. `local-media.json` connects records to site-local MP4s.
- Shared layout and behavior are in `dist/style.css`, `dist/app.js`, and `dist/intro.js`. The logo introduction replays on home refresh and respects reduced motion. Portfolio cards use an on-page video player when a local MP4 exists. Other pieces retain original Wix portfolio links.
- `dist/assets/jhg-share-card-v1.png` is the social link thumbnail. Set `SITE_ORIGIN` before a custom-domain build so the absolute canonical and Open Graph URLs use the final origin.

## Uploaded films

The 32 distinct supplied masters are mapped to Campaigns, Work, AI & Animation, and 3D Rendering. A duplicate Raleigh Firebirds home-dates export is omitted from the catalog. The original masters stay outside this repo. Twelve larger MP4s are served from the companion public JHG media Site; `media-hosted.json` names them and `remote-media-assets.json` pins their checksums. They still play within the portfolio's native player. The main preview stays below its static archive limit. To regenerate full-length, seekable browser MP4s and WebP posters:

```sh
python3 import_videos.py /absolute/path/to/masters
python3 build_site.py
node --check dist/app.js
python3 validate_site.py
```

Publish the generated `dist/assets/media/` with the site. If a Git hosting provider limits binary repository size, host these exact web MP4s on durable static storage and point `local-media.json` to their URL; keep playback in the site's native player and verify seeking. Do not use an expiring Wix stream URL.

For the two-Site preview, move the twelve files listed in `media-hosted.json` from the regenerated main `dist/assets/media/` to the companion media Site before packaging either Site. `fetch_hosted_assets.py` restores both sets into a single `dist/` for the GitHub Pages build. The GitHub artifact is therefore self-contained at deployment time even though large videos are not committed to Git history.

The title film uses ten seconds of existing footage followed by five-second excerpts from the supplied campaign films. Additional source-listed campaign films can be added when their masters arrive. The following three uploads were lost during transfer and need to be attached again: `12-WHISKY-STICKS-POLITICS-SHOUT-OUT-PROMO.webm`, `14-JHG-A.i.-Productions-Presents_-VELLE-S-TALES-THE-MICHAEL-JORDAN-STORY.webm`, and `15-Velle-s-Tales_The-Michael-Jackson-Story-Presented-By-Jhg-A.i.-Animated-Studios.webm`.

## Checks and deployment

The site has no build dependencies beyond Python, Node for syntax checking, and FFmpeg when regenerating video. `dist/` is deployable as a static root. `.openai/hosting.json` identifies the Sites preview. A custom-domain cutover requires the owner's exact hostname and DNS provider. The current Wix site and DNS should remain live during review.

The contact form prepares a mailto message and offers a copyable brief; it does not send through a backend. Motion controls, keyboard dismissal, and responsive layouts are implemented. Validate on actual phone, tablet, and desktop browsers before domain cutover.
