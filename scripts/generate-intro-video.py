"""Generate cinematic intro + footer MP4s from Srivardhan's portfolio photos."""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageEnhance
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', 'imageio', 'imageio-ffmpeg', '-q'])
    from PIL import Image, ImageEnhance

import imageio.v2 as imageio
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'public' / 'assets'

W, H = 1280, 720
FPS = 24

INTRO_CLIPS = [
    {'file': 'hero-foreground.png', 'focus_x': 0.55, 'focus_y': 0.32, 'seconds': 5, 'zoom_end': 1.1, 'pan_x': 0.02},
    {'file': 'photo-casual.png', 'focus_x': 0.5, 'focus_y': 0.35, 'seconds': 4, 'zoom_end': 1.08, 'pan_x': 0.015},
    {'file': 'photo-bw-dramatic.png', 'focus_x': 0.5, 'focus_y': 0.4, 'seconds': 4, 'zoom_end': 1.07, 'pan_x': -0.01},
    {'file': 'photo-campus-night.png', 'focus_x': 0.48, 'focus_y': 0.22, 'seconds': 5, 'zoom_end': 1.09, 'pan_x': 0.012},
]

FOOTER_CLIPS = [
    {'file': 'photo-casual.png', 'focus_x': 0.5, 'focus_y': 0.3, 'seconds': 6, 'zoom_end': 1.06, 'pan_x': 0.01},
    {'file': 'srivardhan-about.png', 'focus_x': 0.5, 'focus_y': 0.24, 'seconds': 6, 'zoom_end': 1.05, 'pan_x': -0.008},
]


def prepare_base(img_path: Path, focus_x: float, focus_y: float) -> np.ndarray:
    img = Image.open(img_path).convert('RGB')
    src_w, src_h = img.size
    scale = max(W / src_w, H / src_h) * 1.22
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.uint8)
    arr = np.array(ImageEnhance.Contrast(Image.fromarray(arr)).enhance(1.05), dtype=np.uint8)
    return arr


def frame_from_base(base: np.ndarray, progress: float, zoom_end: float, pan_x: float, focus_x: float, focus_y: float) -> np.ndarray:
    h, w = base.shape[:2]
    breathe = 0.006 * math.sin(progress * math.pi * 3)
    zoom = 1.0 + (zoom_end - 1.0) * progress + breathe
    crop_w = max(int(w / zoom), W)
    crop_h = max(int(h / zoom), H)
    drift = int(pan_x * w * (progress - 0.5) * 2)
    x0 = max(0, min(int((w - crop_w) * focus_x + drift), w - crop_w))
    y0 = max(0, min(int((h - crop_h) * focus_y), h - crop_h))
    crop = base[y0:y0 + crop_h, x0:x0 + crop_w]
    img = Image.fromarray(crop).resize((W, H), Image.Resampling.BILINEAR)
    return np.array(img)


def crossfade(a: np.ndarray, b: np.ndarray, alpha: float) -> np.ndarray:
    return (a.astype(np.float32) * (1 - alpha) + b.astype(np.float32) * alpha).astype(np.uint8)


def build_clip(clip: dict) -> list[np.ndarray]:
    base = prepare_base(ASSETS / clip['file'], clip['focus_x'], clip['focus_y'])
    total = int(FPS * clip['seconds'])
    return [
        frame_from_base(base, i / max(total - 1, 1), clip['zoom_end'], clip['pan_x'], clip['focus_x'], clip['focus_y'])
        for i in range(total)
    ]


def build_video(clips: list[dict], out_path: Path, fade: int = 12) -> None:
    all_clips = [build_clip(c) for c in clips]
    frames: list[np.ndarray] = []
    n = len(all_clips)
    for i, clip in enumerate(all_clips):
        nxt = all_clips[(i + 1) % n]
        frames.extend(clip)
        for f in range(fade):
            alpha = (f + 1) / fade
            frames.append(crossfade(clip[-1], nxt[0], alpha))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(out_path, frames, fps=FPS, quality=8, macro_block_size=1)
    print(f'Created {out_path} ({len(frames) / FPS:.1f}s, {out_path.stat().st_size // 1024} KB)')


def main() -> None:
    build_video(INTRO_CLIPS, ASSETS / 'about_me.mp4')
    build_video(FOOTER_CLIPS, ASSETS / 'footer-video.mp4')


if __name__ == '__main__':
    main()
