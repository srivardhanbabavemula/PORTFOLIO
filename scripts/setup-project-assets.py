"""Copy original project panel images (no resize) and generate themed backgrounds."""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', '-q'])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(
    r"C:\Users\SRIVARDHANBABAVEMULA\.cursor\projects"
    r"\e-cinematic-portfolio-cinematic-portfolio-cinematic-portfolio-main\assets"
)
PANEL_OUT = ROOT / 'public' / 'assets' / 'projects'
BG_OUT = ROOT / 'public' / 'assets' / 'projects' / 'bg'
PROFILE = ROOT / 'data' / 'profile.json'

# fragment in source filename -> panel output filename
PANEL_COVERS = {
    'ChatGPT_Image_Jun_25__2026__02_13_38_PM-3ca266f7': 'ai-chatbot.png',
    'ChatGPT_Image_Jun_25__2026__02_13_04_PM-55588735': 'rag-qa.png',
    'ChatGPT_Image_Jun_25__2026__02_13_45_PM-f5cefb9d': 'streaming.png',
    'ChatGPT_Image_Jun_25__2026__02_13_41_PM-92506bef': 'kafka-streams.png',
    'ChatGPT_Image_Jun_25__2026__02_13_39_PM-50bb242a': 'airflow.png',
    'ChatGPT_Image_Jun_25__2026__02_13_40_PM-3e6efdf8': 'azure-etl.png',
    'ChatGPT_Image_Jun_25__2026__02_13_43_PM-dcbdaef6': 'pyspark.png',
    'ChatGPT_Image_Jun_25__2026__02_13_10_PM-8f2d6a9d': 'analytics.png',
    'ChatGPT_Image_Jun_25__2026__02_13_17_PM-ff30e119': 'forecasting.png',
    'ChatGPT_Image_Jun_25__2026__09_37_22_PM-134ebc21': 'recommendation.png',
    'ChatGPT_Image_Jun_25__2026__02_13_14_PM-52f386af': 'sentiment.png',
    'ChatGPT_Image_Jun_25__2026__02_13_46_PM-4c2fae24': 'web-scraping.png',
    'ChatGPT_Image_Jun_25__2026__02_13_05_PM-9fdc27ca': 'graph-fraud.png',
    'image-aa0b55ca-cfe2-4b64-a87c-7d814bd5835d': 'deep-o-meter.png',
}

TITLE_TO_FILE = {
    'AI Data Analyst Chatbot': 'ai-chatbot.png',
    'RAG Document Q&A': 'rag-qa.png',
    'Real-Time Streaming': 'streaming.png',
    'Kafka Streams': 'kafka-streams.png',
    'Airflow Data Pipelines': 'airflow.png',
    'Azure Data Factory ETL': 'azure-etl.png',
    'PySpark Processing': 'pyspark.png',
    'Analytics Dashboard': 'analytics.png',
    'Financial Forecasting': 'forecasting.png',
    'Recommendation System': 'recommendation.png',
    'Sentiment Analysis': 'sentiment.png',
    'Web Scraping Pipeline': 'web-scraping.png',
    'Graph ML Fraud Detection': 'graph-fraud.png',
    'Deep-O-Meter': 'deep-o-meter.png',
}

BG_THEMES = {
    'ai-chatbot':       ((30, 58, 138), (99, 102, 241), 'Generative AI · NL-SQL'),
    'rag-qa':           ((15, 118, 110), (45, 212, 191), 'RAG · Vector Search'),
    'streaming':        ((180, 83, 9), (251, 146, 60), 'Kafka · Spark Streaming'),
    'kafka-streams':    ((154, 52, 18), (249, 115, 22), 'Event-Driven Architecture'),
    'airflow':          ((21, 128, 61), (74, 222, 128), 'Workflow Orchestration'),
    'azure-etl':        ((30, 64, 175), (96, 165, 250), 'Azure Data Factory'),
    'pyspark':          ((124, 45, 18), (251, 191, 36), 'Distributed PySpark'),
    'analytics':        ((76, 29, 149), (167, 139, 250), 'Business Intelligence'),
    'forecasting':      ((22, 78, 99), (56, 189, 248), 'Time Series ML'),
    'recommendation':   ((88, 28, 135), (192, 132, 252), 'Collaborative Filtering'),
    'sentiment':        ((190, 24, 93), (244, 114, 182), 'NLP · Sentiment'),
    'web-scraping':     ((55, 65, 81), (148, 163, 184), 'Web Data Pipeline'),
    'graph-fraud':      ((127, 29, 29), (248, 113, 113), 'Graph ML · Fraud'),
    'deep-o-meter':     ((15, 23, 42), (59, 130, 246), 'Deepfake Detection · UB Research'),
}

BG_W, BG_H = 1920, 1080


def find_source(fragment: str) -> Path | None:
    matches = list(SRC.glob(f'*{fragment}*.png'))
    return matches[0] if matches else None


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


def draw_nodes(draw: ImageDraw.ImageDraw, cx: int, cy: int, n: int, r: int) -> None:
    for i in range(n):
        ang = (2 * math.pi * i) / n - math.pi / 2
        x = cx + int(math.cos(ang) * r)
        y = cy + int(math.sin(ang) * r)
        draw.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(255, 255, 255, 55))
        draw.line((cx, cy, x, y), fill=(255, 255, 255, 45), width=3)


def make_background(slug: str, c1: tuple, c2: tuple, label: str) -> None:
    img = gradient((BG_W, BG_H), c1, c2)
    draw = ImageDraw.Draw(img, 'RGBA')

    for x in range(0, BG_W, 64):
        draw.line((x, 0, x, BG_H), fill=(255, 255, 255, 12))
    for y in range(0, BG_H, 64):
        draw.line((0, y, BG_W, y), fill=(255, 255, 255, 12))

    cx, cy = BG_W // 2 + 200, BG_H // 2
    if 'kafka' in slug or 'streaming' in slug:
        for i in range(6):
            y = 180 + i * 130
            draw.rounded_rectangle((200, y, BG_W - 200, y + 36), radius=18, fill=(255, 255, 255, 28))
    elif 'azure' in slug or 'airflow' in slug:
        for i in range(5):
            x = 240 + i * 280
            draw.rounded_rectangle((x, 220, x + 180, 520), radius=16, fill=(255, 255, 255, 32))
    elif 'graph' in slug or 'recommendation' in slug:
        draw_nodes(draw, cx, cy, 10, 280)
    elif 'analytics' in slug or 'forecasting' in slug:
        pts = [(180, 720), (380, 560), (560, 620), (760, 420), (980, 500), (1200, 340), (1500, 400)]
        draw.line(pts, fill=(255, 255, 255, 140), width=5)
        for p in pts:
            draw.ellipse((p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10), fill=(255, 255, 255, 200))
    elif 'deep' in slug:
        draw.ellipse((cx - 220, cy - 220, cx + 220, cy + 220), outline=(255, 255, 255, 80), width=4)
        draw.ellipse((cx - 90, cy - 90, cx + 90, cy + 90), fill=(255, 255, 255, 35))
        draw.line((cx - 130, cy, cx + 130, cy), fill=(255, 255, 255, 60), width=2)
        draw.line((cx, cy - 130, cx, cy + 130), fill=(255, 255, 255, 60), width=2)
    elif 'sentiment' in slug or 'rag' in slug or 'ai' in slug:
        draw.rounded_rectangle((320, 240, BG_W - 320, 720), radius=32, fill=(255, 255, 255, 22), outline=(255, 255, 255, 60), width=2)
        for ly in range(300, 640, 56):
            draw.rounded_rectangle((380, ly, BG_W - 380, ly + 22), radius=11, fill=(255, 255, 255, 40))
    else:
        draw.ellipse((cx - 180, cy - 180, cx + 180, cy + 180), outline=(255, 255, 255, 55), width=3)

    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except OSError:
        font = ImageFont.load_default()

    draw.rounded_rectangle((80, BG_H - 120, 80 + 520, BG_H - 48), radius=20, fill=(255, 255, 255, 35))
    draw.text((108, BG_H - 102), label, fill=(255, 255, 255, 230), font=font)

    BG_OUT.mkdir(parents=True, exist_ok=True)
    out = BG_OUT / f'{slug}-bg.png'
    img.save(out, optimize=True)
    print(f'Background {out.name}')


def copy_panels() -> None:
    PANEL_OUT.mkdir(parents=True, exist_ok=True)
    for fragment, dst_name in PANEL_COVERS.items():
        src = find_source(fragment)
        if not src:
            print(f'MISSING panel: {fragment}')
            continue
        shutil.copy2(src, PANEL_OUT / dst_name)
        print(f'Panel {dst_name} <- {src.name[:56]}...')


def update_profile() -> None:
    data = json.loads(PROFILE.read_text(encoding='utf-8'))
    for proj in data['projects']:
        fname = next((f for k, f in TITLE_TO_FILE.items() if k in proj['title']), None)
        if not fname:
            print(f'No file mapping: {proj["title"]}')
            continue
        slug = fname.replace('.png', '')
        proj['image'] = f'/assets/projects/{fname}'
        proj['bgImage'] = f'/assets/projects/bg/{slug}-bg.png'
        proj.pop('bgImagePosition', None)
    PROFILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Updated {len(data["projects"])} projects in profile.json')


def main() -> None:
    copy_panels()
    for slug, (c1, c2, label) in BG_THEMES.items():
        make_background(slug, c1, c2, label)
    update_profile()


if __name__ == '__main__':
    main()
