#!/usr/bin/env python3
"""Shrink in-article images in place, conservatively.

Article bodies render at ~800px wide, so anything wider than MAX_W (2x for
retina) is carrying pixels no reader ever sees. Beyond downscaling, the big
win is PNGs that should never have been PNGs: AI illustrations and photos,
where palette quantization saves 60-80%. Screenshots are the risky case —
text must stay crisp — so quantization is only accepted when it beats the
lossless re-encode by a wide margin, and every rewrite must clear a minimum
saving or the original file is left untouched.

Formats and filenames never change, so markdown references are safe. SVG,
GIF (animation), WebP and cover images (featured.jpg) are left alone.

    python3 .github/scripts/shrink_article_images.py           # whole site
    python3 .github/scripts/shrink_article_images.py content/posts/2026
"""

import io
import os
import sys

from PIL import Image

MAX_W = 1600          # 2x the ~800px article column
MIN_SIZE = 150 * 1024  # leave small files alone
MIN_SAVING = 0.10      # a rewrite must save at least this fraction
QUANT_MARGIN = 0.60    # quantized PNG must be <= 60% of the lossless size
JPEG_QUALITY = 85


def downscale(im):
    if im.width > MAX_W:
        h = round(im.height * MAX_W / im.width)
        return im.resize((MAX_W, h), Image.LANCZOS)
    return im


def encode_jpeg(im):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return buf.getvalue()


def encode_png(im):
    """Return the best acceptable PNG encoding: lossless, or a palette
    version only when it wins by enough to be worth the risk."""
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    base = im.convert("RGBA" if has_alpha else "RGB")

    buf = io.BytesIO()
    base.save(buf, "PNG", optimize=True)
    lossless = buf.getvalue()

    try:
        quant = base.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        qbuf = io.BytesIO()
        quant.save(qbuf, "PNG", optimize=True)
        quantized = qbuf.getvalue()
    except Exception:
        return lossless

    if len(quantized) <= len(lossless) * QUANT_MARGIN:
        return quantized
    return lossless


def process(path):
    size = os.path.getsize(path)
    if size < MIN_SIZE:
        return None
    ext = path.rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg"):
        return None
    if os.path.basename(path) == "featured.jpg":
        return None

    im = Image.open(path)
    im = downscale(im)
    data = encode_png(im) if ext == "png" else encode_jpeg(im)

    if len(data) > size * (1 - MIN_SAVING):
        return (path, size, size, False)  # not worth rewriting
    with open(path, "wb") as f:
        f.write(data)
    return (path, size, len(data), True)


CONVERT_THRESHOLD = 800 * 1024


def uses_alpha(im):
    if im.mode in ("RGBA", "LA"):
        lo, _ = im.getchannel("A").getextrema()
        return lo < 250
    return im.mode == "P" and "transparency" in im.info


def convert_stubborn(root="content"):
    """Second pass: PNGs still huge after the in-format pass are photographic
    content in the wrong container. Convert them to JPEG and rewrite the
    markdown references — but only when the image has no transparency and is
    referenced nowhere outside its own bundle, so the rename cannot break a
    link the rewrite does not see."""
    all_md = []
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".md"):
                all_md.append(os.path.join(d, f))

    for d, _, fs in os.walk(root):
        for f in sorted(fs):
            if not f.endswith(".png"):
                continue
            path = os.path.join(d, f)
            if os.path.getsize(path) < CONVERT_THRESHOLD:
                continue
            im = Image.open(path)
            if uses_alpha(im):
                print(f"  skip (alpha): {path}")
                continue
            newname = f[:-4] + ".jpg"
            if os.path.exists(os.path.join(d, newname)):
                print(f"  skip (name taken): {path}")
                continue

            local_md = [m for m in all_md if os.path.dirname(m) == d]
            foreign = [
                m for m in all_md
                if m not in local_md and f in open(m, encoding="utf-8").read()
            ]
            if foreign:
                print(f"  skip (referenced outside bundle): {path}")
                continue

            data = encode_jpeg(downscale(im))
            if len(data) > os.path.getsize(path) * (1 - MIN_SAVING):
                continue
            with open(os.path.join(d, newname), "wb") as out:
                out.write(data)
            os.remove(path)
            for m in local_md:
                text = open(m, encoding="utf-8").read()
                if f in text:
                    open(m, "w", encoding="utf-8").write(text.replace(f, newname))
            print(f"  {len(data) // 1024:6} KB  {path} -> {newname}")


def main():
    if "--convert" in sys.argv:
        convert_stubborn()
        return
    roots = sys.argv[1:] or ["content"]
    results = []
    for root in roots:
        for d, _, fs in os.walk(root):
            for f in sorted(fs):
                r = process(os.path.join(d, f))
                if r:
                    results.append(r)

    rewritten = [r for r in results if r[3]]
    kept = [r for r in results if not r[3]]
    before = sum(r[1] for r in rewritten)
    after = sum(r[2] for r in rewritten)
    for path, b, a, _ in sorted(rewritten, key=lambda r: r[2] - r[1]):
        print(f"  {b // 1024:6} KB -> {a // 1024:6} KB  {path}")
    print(f"\nrewrote {len(rewritten)} file(s): {before / 1e6:.1f} MB -> {after / 1e6:.1f} MB")
    print(f"left {len(kept)} candidate(s) unchanged (saving under {MIN_SAVING:.0%})")


if __name__ == "__main__":
    main()
