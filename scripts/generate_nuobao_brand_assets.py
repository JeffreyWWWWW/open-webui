from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


TARGETS = {
    'logo.png': 512,
    'favicon.png': 512,
    'favicon-96x96.png': 96,
    'apple-touch-icon.png': 180,
    'web-app-manifest-192x192.png': 192,
    'web-app-manifest-512x512.png': 512,
    'splash.png': 512,
    'splash-dark.png': 512,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=Path('static/static'))
    args = parser.parse_args()

    image = Image.open(args.source).convert('RGBA')
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for name, size in TARGETS.items():
        image.resize((size, size), Image.Resampling.LANCZOS).save(args.output_dir / name)

    image.save(args.output_dir / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])


if __name__ == '__main__':
    main()
