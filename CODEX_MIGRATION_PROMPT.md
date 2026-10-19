# Codex handoff — JHG Productions

I own JHG Productions. Continue work on `mosdefjg/JHG-PRODUCTIONS`, starting from the `codex/jhg-site-redesign` branch and its reviewable pull request. The site is an eight-page static HTML/CSS/JS project. `dist/` is the deployable root; `build_site.py`, the JSON catalogues, and `intro.html` generate pages. Keep unrelated repository history intact.

Run `python3 build_site.py`, `node --check dist/app.js`, and `python3 validate_site.py`. Review Home, Work, Campaigns, AI & Animation, 3D Rendering, Services, About, Contact on mobile, tablet, and desktop. Preserve the three-logo intro on first visit and every home refresh, moving title video, native Meet JHG player, share card metadata, keyboard controls, and reduced-motion behavior. Keep the cinematic dark palette with subtle orange, white, and blue accents.

The video inventory is in `video-imports.json`. Uploaded masters are intentionally outside the public site. `import_videos.py /path/to/masters` produces seekable H.264/AAC MP4s and WebP posters at `dist/assets/media/`; `local-media.json` maps the resulting site-local URLs. The catalogue is grouped across Campaigns, AI & Animation, 3D Rendering, and Work. Native video players are in `dist/app.js`. Check that playback and seeking work on mobile as well as desktop. Do not route imported films to Wix or YouTube.

The opening montage should keep ten seconds of the original title film followed by five seconds from each locally supplied campaign video. Keep the motion transitions smooth and avoid black frames. Update the hero's source only after the finished montage is packaged and verified.

The GitHub Pages workflow publishes `dist/` at a domain root. Before setting a custom domain, ask which exact hostname and DNS provider I control; do not assume `jhgfilms.com` is mine. Set the `SITE_ORIGIN` Actions variable to that final HTTPS origin so canonical links and the share card use the custom URL. Review a preview before changing DNS. No domain cutover is authorized by this prompt alone.

Three videos from a later upload did not survive the transfer and must be reattached to include them: `12-WHISKY-STICKS-POLITICS-SHOUT-OUT-PROMO.webm`, `14-JHG-A.i.-Productions-Presents_-VELLE-S-TALES-THE-MICHAEL-JORDAN-STORY.webm`, and `15-Velle-s-Tales_The-Michael-Jackson-Story-Presented-By-Jhg-A.i.-Animated-Studios.webm`. Keep their existing Wix portfolio entries until playable files are supplied.

Deliver a working site link, a PR link, results of the checks, and any remaining domain or media inputs.
