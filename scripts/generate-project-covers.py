"""Generate clean abstract cover art for portfolio project slides."""
from __future__ import annotations

import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', '-q'])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public' / 'assets' / 'projects'
W, H = 960, 640

THEMES = {
    'ai-chatbot':       ((30, 58, 138), (99, 102, 241), 'AI / NL-SQL'),
    'rag-qa':           ((15, 118, 110), (45, 212, 191), 'RAG / Docs'),
    'streaming':        ((180, 83, 9), (251, 146, 60), 'Kafka / Spark'),
    'kafka-streams':    ((154, 52, 18), (249, 115, 22), 'Event Streams'),
    'airflow':          ((21, 128, 61), (74, 222, 128), 'Airflow DAGs'),
    'azure-etl':        ((30, 64, 175), (96, 165, 250), 'Azure ETL'),
    'pyspark':          ((124, 45, 18), (251, 191, 36), 'PySpark'),
    'analytics':        ((76, 29, 149), (167, 139, 250), 'BI Dashboard'),
    'forecasting':      ((22, 78, 99), (56, 189, 248), 'Forecasting'),
    'recommendation':   ((88, 28, 135), (192, 132, 252), 'RecSys'),
    'sentiment':        ((190, 24, 93), (244, 114, 182), 'NLP Sentiment'),
    'web-scraping':     ((55, 65, 81), (148, 163, 184), 'Web ETL'),
    'graph-fraud':      ((127, 29, 29), (248, 113, 113), 'Graph ML'),
    'deep-o-meter':     ((15, 23, 42), (71, 85, 105), 'Deepfake AI'),
}


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient(size: tuple[int, int], c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new('RGB', size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        row = (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))
        for x in range(w):
            px[x, y] = row
    return img


def draw_nodes(draw: ImageDraw.ImageDraw, cx: int, cy: int, n: int, r: int, color: tuple[int, int, int, int]) -> None:
    for i in range(n):
        ang = (2 * math.pi * i) / n - math.pi / 2
        x = cx + int(math.cos(ang) * r)
        y = cy + int(math.sin(ang) * r)
        draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color)
        draw.line((cx, cy, x, y), fill=(*color[:3], 80), width=2)


def make_cover(slug: str, c1: tuple, c2: tuple, label: str) -> None:
    img = gradient((W, H), c1, c2)
    draw = ImageDraw.Draw(img, 'RGBA')

    # soft grid
    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill=(255, 255, 255, 18))
    for y in range(0, H, 48):
        draw.line((0, y, W, y), fill=(255, 255, 255, 18))

    # decorative shapes per theme family
    if 'kafka' in slug or 'streaming' in slug:
        for i in range(5):
            y = 120 + i * 90
            draw.rounded_rectangle((120, y, W - 120, y + 28), radius=14, fill=(255, 255, 255, 35))
    elif 'azure' in slug or 'airflow' in slug:
        for i in range(4):
            x = 160 + i * 170
            draw.rounded_rectangle((x, 180, x + 120, 380), radius=12, fill=(255, 255, 255, 40))
    elif 'graph' in slug or 'recommendation' in slug:
        draw_nodes(draw, W // 2, H // 2 - 20, 8, 160, (255, 255, 255, 90))
    elif 'analytics' in slug or 'forecasting' in slug:
        pts = [(140, 420), (260, 320), (380, 360), (520, 220), (660, 280), (820, 180)]
        draw.line(pts, fill=(255, 255, 255, 180), width=4)
        for p in pts:
            draw.ellipse((p[0] - 8, p[1] - 8, p[0] + 8, p[1] + 8), fill=(255, 255, 255, 220))
    elif 'sentiment' in slug or 'rag' in slug or 'ai' in slug:
        draw.rounded_rectangle((180, 160, W - 180, 420), radius=24, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=2)
        for ly in range(210, 380, 42):
            draw.rounded_rectangle((220, ly, W - 220, ly + 18), radius=9, fill=(255, 255, 255, 55))
    else:
        draw.ellipse((W // 2 - 120, H // 2 - 120, W // 2 + 120, H // 2 + 120), outline=(255, 255, 255, 70), width=3)

    # label pill
    try:
        font = ImageFont.truetype('arial.ttf', 28)
        small = ImageFont.truetype('arial.ttf', 20)
    except OSError:
        font = ImageFont.load_default()
        small = font

    draw.rounded_rectangle((48, H - 88, 48 + 280, H - 36), radius=16, fill=(255, 255, 255, 45))
    draw.text((68, H - 78), label, fill=(255, 255, 255, 240), font=small)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f'{slug}.png'
    img.save(path, optimize=True)
    print(f'Created {path}')


def main() -> None:
    for slug, (c1, c2, label) in THEMES.items():
        make_cover(slug, c1, c2, label)


if __name__ == '__main__':
    main()
