# picfit 🖼️⚡

**Batch resize & convert photos in seconds — 100% offline, EXIF/GPS stripped by default.**

Sending 20 photos by e-mail? Uploading to a portal that rejects >2 MB? Posting
photos online without leaking your **GPS location**? One command:

```bash
python picfit.py ./Photos --max 1920 --apply      # longest side 1920px
python picfit.py ./DCIM --format webp --apply     # convert folder to WebP
python picfit.py IMG_*.jpg --percent 40 --apply   # shrink to 40 %
python picfit.py selfie.jpg                       # just strip GPS/EXIF, keep size
```

```
✔ big.png: 4000x2000 -> 1920x960  106.1 KB -> 30.5 KB, exif stripped
✔ mid.jpg: 1600x900 -> 800x450 -> WEBP  44.9 KB -> 7.1 KB, exif stripped
```

---

## Why?

- Online resizers = **uploading your private photos to strangers' servers**.
- Photo editors = overkill for "make these smaller".
- And almost nobody knows their photos **carry GPS coordinates and camera serials**
  when posted online. `picfit` removes that by default.

## Privacy

| | Default | `--keep-exif` |
|---|---|---|
| GPS location | ❌ removed | ✅ kept |
| Camera make/serial | ❌ removed | ✅ kept |
| Date taken | ❌ removed | ✅ kept |

Verified by test: metadata written into a JPEG comes out **empty** after `picfit`.

## Install

```bash
pip install pillow
curl -LO https://raw.githubusercontent.com/Volvox6767/picfit/main/picfit.py
```

One dependency (Pillow), one file.

## Usage

```
python picfit.py INPUT... [--max PX | --percent N | --width PX | --height PX]
                   [--format jpg|png|webp] [--quality N] [--out DIR]
                   [--apply] [--keep-exif] [--recursive]

INPUT...      image files and/or folders
--max PX      longest side becomes PX (keeps aspect, never upscales)
--percent N   scale to N %
--width/--height PX   set one side, keep aspect
--format      convert: jpg / png / webp
--quality     JPEG/WebP quality (default 85)
--out DIR     write results to DIR instead of *_fit.* files
--apply       really write (default: dry-run preview)
--keep-exif   keep metadata (default: strip)
```

Input formats: jpg, png, webp, bmp, gif, tiff. Output: jpg / png / webp.

With **no resize option**, picfit runs in *privacy mode*: re-saves every photo
same-size with metadata stripped.

## Notes

- Animated GIFs are skipped (safety).
- Dry-run preview by default — nothing is written until `--apply`.
- Originals are never touched: results go to `*_fit.*` or `--out DIR`.

## FAQ

**Will it ruin quality?** LANCZOS resampling + optimized JPEG/WebP. 85 quality is visually transparent for sharing.

**Upscaling?** Never — smaller images are left as-is.

---

Made with ❤ by **Ahmet Gedik** — [instagram.com/ahmetgedik67](https://www.instagram.com/ahmetgedik67)
Follow on Instagram for more free everyday tools.

License: [MIT](LICENSE)
