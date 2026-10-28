"""Build web-sized images in public/assets from the originals in brand/.

Run from the repo root: python3 scripts/optimize_images.py
Requires Pillow (pip install Pillow). Logos are only resized and palette-compressed,
never recolored.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand"
OUT = ROOT / "public" / "assets"
PUBLIC = ROOT / "public"

DARK_BLUE = (10, 41, 59)


def fit_height(im, height):
    width = round(im.width * height / im.height)
    return im.resize((width, height), Image.LANCZOS)


def save_png(im, path, colors=256):
    # Palette PNG with alpha keeps edges clean and cuts file size sharply.
    q = im.convert("RGBA").quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q.save(path, optimize=True)
    print(f"{path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB  {im.size}")


def crop_mark(lockup):
    """Crop the mark: everything left of the first fully transparent column."""
    alpha = lockup.getchannel("A")
    for x in range(1, lockup.width):
        if alpha.crop((x, 0, x + 1, lockup.height)).getextrema()[1] == 0:
            return lockup.crop((0, 0, x, lockup.height)).crop(alpha.crop((0, 0, x, lockup.height)).getbbox())
    raise ValueError("no gap between mark and wordmark")


def square(im):
    side = max(im.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    return canvas


def on_background(mark, size, bg, padding):
    canvas = Image.new("RGBA", (size, size), bg + (255,))
    inner = size - 2 * padding
    m = mark.copy()
    m.thumbnail((inner, inner), Image.LANCZOS)
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Logo is shown at 64px (header) and 44px (footer); 2x for retina.
    dark = Image.open(SRC / "zare-logo-dark.png").convert("RGBA")
    save_png(fit_height(dark, 128), OUT / "zare-logo-dark.png")

    # Favicons from the navy mark. The supplied bolt-*.png files are solid
    # rectangles with no bolt in them, so the mark is cropped (not redrawn)
    # from the navy lockup instead.
    light = Image.open(SRC / "zare-logo-light.png").convert("RGBA")
    bolt = square(crop_mark(light))
    bolt.resize((48, 48), Image.LANCZOS).save(
        PUBLIC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("public/favicon.ico")
    save_png(bolt.resize((32, 32), Image.LANCZOS), PUBLIC / "favicon-32.png")
    # Touch icons need an opaque background.
    save_png(on_background(bolt, 180, (255, 255, 255), 24), PUBLIC / "apple-touch-icon.png")
    save_png(on_background(bolt, 512, (255, 255, 255), 64), PUBLIC / "icon-512.png")

    # Open Graph share image: dark-blue field with the dark-background logo.
    og = Image.new("RGBA", (1200, 630), DARK_BLUE + (255,))
    logo = fit_height(dark, 240)
    og.alpha_composite(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2))
    og.convert("RGB").save(OUT / "og-image.png", optimize=True)
    print(f"public/assets/og-image.png  {(OUT / 'og-image.png').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
