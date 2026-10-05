#!/usr/bin/env python3
"""
picfit — batch resize & convert photos in seconds. Privacy-first: runs 100% local.

  python picfit.py ./Photos --max 1920              # longest side 1920px
  python picfit.py IMG_*.jpg --percent 40           # shrink to 40%
  python picfit.py ./DCIM --format webp --apply     # convert whole folder to WebP
  python picfit.py a.jpg b.png --max 800 --apply

EXIF (GPS location, serial numbers...) is REMOVED by default.
Pass --keep-exif if you want to preserve it.

Needs Pillow:  pip install pillow
Author : Ahmet Gedik  (https://www.instagram.com/ahmetgedik67)
License: MIT
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

__version__ = "1.0.0"
AUTHOR = "Ahmet Gedik"
INSTAGRAM = "https://www.instagram.com/ahmetgedik67"

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "picfit needs Pillow (one-time):\n"
        "  pip install pillow\n"
        "then run picfit again."
    )

Image.MAX_IMAGE_PIXELS = 300_000_000  # allow huge panoramas, still safe

IN_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff", ".tif"}
FORMATS = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}


def banner() -> str:
    return (
        "\n  picfit — batch resize & convert photos, 100% offline\n"
        f"  by {AUTHOR}  |  {INSTAGRAM}\n"
        "  -----------------------------------------------------\n"
    )


def human(n: float) -> str:
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{int(n)} B" if u == "B" else f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} GB"


def collect(inputs: list[str], recursive: bool) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            it = p.rglob("*") if recursive else p.iterdir()
            files += [f for f in sorted(it) if f.is_file() and f.suffix.lower() in IN_EXT]
        elif p.exists():
            files.append(p)
        else:
            print(f"  ! not found: {item}")
    # dedupe, keep order
    seen, out = set(), []
    for f in files:
        r = f.resolve()
        if r not in seen:
            seen.add(r)
            out.append(f)
    return out


def new_size(w: int, h: int, args) -> tuple[int, int]:
    if args.percent:
        s = args.percent / 100.0
        return max(1, round(w * s)), max(1, round(h * s))
    if args.max:
        # longest side -> args.max, keep aspect
        if w >= h:
            return (args.max, max(1, round(h * args.max / w))) if w > args.max else (w, h)
        return (max(1, round(w * args.max / h)), args.max) if h > args.max else (w, h)
    if args.width:
        return args.width, max(1, round(h * args.width / w))
    if args.height:
        return max(1, round(w * args.height / h)), args.height
    return w, h


def out_path(src: Path, args) -> Path:
    ext = f".{args.format}" if args.format else src.suffix
    if args.out:
        d = Path(args.out)
        d.mkdir(parents=True, exist_ok=True)
        return d / f"{src.stem}{ext}"
    return src.with_name(f"{src.stem}_fit{ext}")


def save(img: Image.Image, dst: Path, src_fmt: str, args) -> None:
    fmt = FORMATS.get((args.format or src_fmt).lower(), src_fmt.upper().lstrip("."))
    kw: dict = {}
    if fmt == "JPEG":
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        kw = {"quality": args.quality, "optimize": True, "progressive": True}
    elif fmt == "WEBP":
        if img.mode not in ("RGB", "RGBA", "L"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        kw = {"quality": args.quality, "method": 4}
    elif fmt == "PNG":
        kw = {"optimize": True}
    save_kw = dict(kw)
    if not args.keep_exif:
        save_kw["exif"] = b""
    try:
        img.save(dst, fmt, **save_kw)
    except TypeError:      # format ignores some kwargs
        img.save(dst, fmt)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="picfit",
        description="Batch resize & convert photos offline. EXIF/GPS stripped by default.",
        epilog=f"by {AUTHOR} — {INSTAGRAM}",
    )
    ap.add_argument("inputs", nargs="+", help="image files and/or folders")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--max", type=int, metavar="PX", help="longest side -> PX (keeps aspect)")
    g.add_argument("--percent", type=int, metavar="N", help="scale to N%%")
    g.add_argument("--width", type=int, metavar="PX", help="resize to width PX")
    g.add_argument("--height", type=int, metavar="PX", help="resize to height PX")
    ap.add_argument("--format", choices=["jpg", "png", "webp"], help="convert to this format")
    ap.add_argument("--quality", type=int, default=85, help="JPEG/WebP quality (default 85)")
    ap.add_argument("--out", metavar="DIR", help="write results into DIR instead of *_fit files")
    ap.add_argument("--apply", action="store_true",
                    help="really write files (default: preview only)")
    ap.add_argument("--keep-exif", action="store_true",
                    help="keep EXIF metadata (default: strip GPS & personal data)")
    ap.add_argument("--recursive", "-r", action="store_true", help="descend into subfolders")
    ap.add_argument("--version", action="version", version=f"picfit {__version__}")
    args = ap.parse_args()

    if not any([args.max, args.percent, args.width, args.height, args.format]):
        print("no resize/convert option given → EXIF/GPS privacy-clean mode "
              "(re-save in place size, strip metadata):\n")

    print(banner())
    files = collect(args.inputs, args.recursive)
    if not files:
        print("no images found.")
        return 1

    print(f"{'PREVIEW (nothing written — add --apply)' if not args.apply else 'processing...'}\n")
    ok = saved_total = orig_total = errors = 0
    for f in files:
        try:
            with Image.open(f) as im:
                w0, h0 = im.size
                fmt0 = (im.format or f.suffix.lstrip(".")).lower()
                animated = getattr(im, "is_animated", False)
                has_exif_probe = bool(im.getexif()) if not args.keep_exif else False
            if animated:
                print(f"  ~ {f.name}: animated — skipped (safety)")
                continue
            w1, h1 = new_size(w0, h0, args)
            dst = out_path(f, args)
            has_exif = bool(im.getexif()) if not args.keep_exif else False
            changed = (w1, h1) != (w0, h0) or dst.suffix.lower() != f.suffix.lower() or has_exif
            if not changed and dst == f.with_name(f"{f.stem}_fit{f.suffix}"):
                print(f"  = {f.name}: already fits, skipped")
                continue
            est = f"{w0}x{h0} -> {w1}x{h1}" if (w1, h1) != (w0, h0) else f"{w0}x{h0}"
            conv = f" -> {dst.suffix.lstrip('.').upper()}" if dst.suffix.lower() != f.suffix.lower() else ""
            exif = ", exif kept" if args.keep_exif else (", exif stripped" if has_exif_probe else "")
            if not args.apply:
                print(f"  [dry] {f.name}: {est}{conv}{exif}  →  {dst.name}")
                ok += 1
                continue
            with Image.open(f) as im:
                if (w1, h1) != (w0, h0):
                    im = im.resize((w1, h1), Image.LANCZOS)
                save(im, dst, fmt0, args)
            before, after = f.stat().st_size, dst.stat().st_size
            orig_total += before
            saved_total += after
            print(f"  ✔ {f.name}: {est}{conv}  {human(before)} -> {human(after)}{exif}")
            ok += 1
        except Exception as e:
            print(f"  ✘ {f.name}: {e}")
            errors += 1

    if args.apply and orig_total:
        print(f"\ndone: {ok} file(s), {human(orig_total)} -> {human(saved_total)} "
              f"({100 * saved_total / orig_total:.0f}% of original)"
              + (f", {errors} error(s)" if errors else ""))
    elif args.apply:
        print(f"\ndone: {ok} file(s)" + (f", {errors} error(s)" if errors else ""))
    else:
        print(f"\n{ok} file(s) would be processed. 👍 looks right? run again with --apply")
    print(f"\nmade with ❤ by {AUTHOR} — {INSTAGRAM}")
    return 0 if errors == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
