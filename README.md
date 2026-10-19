# JHG Productions website — GitHub export

This is the October 19, 2026 redesign source, built as static HTML/CSS/JS. `dist/` contains the ready-made site; `build_site.py` regenerates the eight pages from the included content and assets. There is no npm dependency or database.

## Run and check

From this directory:

```sh
python3 build_site.py
python3 validate_site.py
```

Deploy the contents of `dist/` as a site at the domain root. The absolute internal links require root hosting. A GitHub Pages Actions workflow is included as a starting point; activate Pages with **GitHub Actions** as its source after merging to the selected repository's default branch. If the repository uses a different branch, adjust the workflow trigger before merging. Preserve existing repository content and deployment workflow when integrating this export.

Set the repository Actions variable `SITE_ORIGIN` to the final URL, including `https://` and without a trailing slash. This regenerates canonical and social preview URLs for the chosen domain. Confirm the domain and DNS provider before changing DNS. GitHub Pages custom domains are configured in repository Settings → Pages; an Actions-based Pages publish does not require a CNAME file.

## Current video status

The 10-second moving title loop and the 2:09 “Meet JHG” film are included locally. Campaign and AI/3D portfolio entries use JHG-owned thumbnails and currently open their Wix collections. Individual video MP4s or verified embed links are still needed for native project playback. The requested montage of 10 seconds of existing footage plus five seconds from each of 46 campaign films cannot be assembled until the source clips arrive. See `VIDEO_IMPORT.md`.

## Content and publishing notes

`dist/assets/` includes branding, images, fonts, and video required by the deployed pages. `jhg-title-continuous.mp4` and `jhg-hero-loop.mp4` are retained source variations for future edits even though the current homepage plays `jhg-title-ten-seconds.mp4`. The original ChatGPT Sites deployment identifier and its Git metadata have intentionally been excluded from this portable export. Keep the current live site online during review and domain cutover.
