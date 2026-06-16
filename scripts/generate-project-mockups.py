"""Generate realistic browser-style project output mockups for portfolio slides."""
from __future__ import annotations

import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "assets" / "projects"
W, H = 1200, 760


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["segoeui.ttf", "Segoe UI.ttf", "arial.ttf", "Arial.ttf"]
    if bold:
        names = ["segoeuib.ttf", "Segoe UI Bold.ttf", "arialbd.ttf"] + names
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def chrome(title: str, accent: tuple[int, int, int]) -> tuple[Image.Image, ImageDraw.ImageDraw, tuple[int, int, int, int]]:
    img = Image.new("RGB", (W, H), (241, 245, 249))
    draw = ImageDraw.Draw(img)
    rounded_rect(draw, (24, 24, W - 24, H - 24), 18, (255, 255, 255), (226, 232, 240), 2)
    # title bar
    rounded_rect(draw, (24, 24, W - 24, 72), 18, (248, 250, 252))
    draw.rectangle((24, 56, W - 24, 72), fill=(248, 250, 252))
    for i, c in enumerate([(239, 68, 68), (234, 179, 8), (34, 197, 94)]):
        draw.ellipse((44 + i * 22, 40, 56 + i * 22, 52), fill=c)
    draw.text((96, 38), title, fill=(15, 23, 42), font=font(16, True))
    draw.rounded_rectangle((W - 180, 36, W - 48, 56), radius=8, fill=(241, 245, 249))
    draw.text((W - 168, 40), "localhost:3000", fill=(100, 116, 139), font=font(11))
    body = (40, 84, W - 40, H - 40)
    rounded_rect(draw, body, 12, (255, 255, 255), (226, 232, 240), 1)
    return img, draw, body


def save(img: Image.Image, slug: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{slug}.png"
    img.save(path, optimize=True)
    print(f"Created {path}")


def mock_chat_sql():
    img, draw, body = chrome("AI Data Analyst — NL to SQL", (59, 130, 246))
    x1, y1, x2, y2 = body
    draw.text((x1 + 24, y1 + 20), "Ask your data", fill=(15, 23, 42), font=font(22, True))
    rounded_rect(draw, (x1 + 24, y1 + 60, x2 - 24, y1 + 110), 12, (239, 246, 255), (191, 219, 254))
    draw.text((x1 + 40, y1 + 78), "Show top 5 products by revenue last quarter", fill=(30, 64, 175), font=font(14))
    rounded_rect(draw, (x1 + 24, y1 + 130, x2 - 24, y1 + 280), 12, (15, 23, 42))
    sql = (
        "SELECT product_name, SUM(revenue) AS total\n"
        "FROM sales\n"
        "WHERE quarter = 'Q4' AND year = 2025\n"
        "GROUP BY product_name\n"
        "ORDER BY total DESC\n"
        "LIMIT 5;"
    )
    draw.multiline_text((x1 + 40, y1 + 150), sql, fill=(226, 232, 240), font=font(13), spacing=6)
    # mini table
    rounded_rect(draw, (x1 + 24, y1 + 300, x2 - 24, y2 - 24), 12, (248, 250, 252), (226, 232, 240))
    headers = ["Product", "Revenue", "Growth"]
    cols = [x1 + 40, x1 + 280, x1 + 420]
    for i, h in enumerate(headers):
        draw.text((cols[i], y1 + 320), h, fill=(100, 116, 139), font=font(12, True))
    rows = [("Cloud ETL Suite", "$1.2M", "+18%"), ("Analytics Pro", "$980K", "+12%"), ("Stream Kit", "$740K", "+24%")]
    for ri, row in enumerate(rows):
        yy = y1 + 350 + ri * 28
        for ci, cell in enumerate(row):
            draw.text((cols[ci], yy), cell, fill=(15, 23, 42), font=font(12))
    save(img, "ai-chatbot")


def mock_rag():
    img, draw, body = chrome("RAG Document Q&A", (13, 148, 136))
    x1, y1, x2, y2 = body
    rounded_rect(draw, (x1 + 20, y1 + 20, x1 + 340, y2 - 20), 10, (240, 253, 250), (153, 246, 228))
    draw.text((x1 + 36, y1 + 36), "Documents", fill=(15, 118, 110), font=font(14, True))
    for i, doc in enumerate(["annual_report.pdf", "product_specs.docx", "faq.md"]):
        rounded_rect(draw, (x1 + 36, y1 + 70 + i * 52, x1 + 320, y1 + 110 + i * 52), 8, (255, 255, 255), (153, 246, 228))
        draw.text((x1 + 48, y1 + 86 + i * 52), doc, fill=(17, 94, 89), font=font(12))
    rounded_rect(draw, (x1 + 360, y1 + 20, x2 - 20, y2 - 20), 10, (255, 255, 255), (226, 232, 240))
    draw.text((x1 + 380, y1 + 36), "Chat", fill=(15, 23, 42), font=font(14, True))
    msgs = [
        ("user", "What were Q3 operating margins?"),
        ("bot", "Based on annual_report.pdf, Q3 operating margin was 23.4%, up 2.1 pts YoY."),
        ("user", "List key risk factors mentioned."),
    ]
    yy = y1 + 70
    for role, text in msgs:
        color = (226, 232, 240) if role == "user" else (204, 251, 241)
        tc = (51, 65, 85) if role == "user" else (17, 94, 89)
        rounded_rect(draw, (x1 + 380, yy, x2 - 40, yy + 56), 10, color)
        draw.text((x1 + 396, yy + 18), text, fill=tc, font=font(12))
        yy += 68
    save(img, "rag-qa")


def mock_streaming():
    img, draw, body = chrome("Real-Time Streaming Platform", (234, 88, 12))
    x1, y1, x2, y2 = body
    cards = [("Events/sec", "512,430", "+12%"), ("Latency p95", "1.8s", "-0.3s"), ("Uptime", "99.92%", "OK")]
    for i, (label, val, delta) in enumerate(cards):
        bx = x1 + 20 + i * 360
        rounded_rect(draw, (bx, y1 + 20, bx + 330, y1 + 110), 12, (255, 247, 237), (254, 215, 170))
        draw.text((bx + 20, y1 + 36), label, fill=(154, 52, 18), font=font(12))
        draw.text((bx + 20, y1 + 58), val, fill=(124, 45, 18), font=font(28, True))
        draw.text((bx + 20, y1 + 88), delta, fill=(234, 88, 12), font=font(11))
    # line chart area
    rounded_rect(draw, (x1 + 20, y1 + 130, x2 - 20, y2 - 80), 12, (255, 255, 255), (254, 215, 170))
    pts = []
    for i in range(12):
        px = x1 + 60 + i * 85
        py = y2 - 120 - int(80 * math.sin(i / 2) + 40 + i * 8)
        pts.append((px, py))
    draw.line(pts, fill=(249, 115, 22), width=3)
    for p in pts:
        draw.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=(234, 88, 12))
    draw.text((x1 + 36, y1 + 146), "Kafka → Spark Streaming throughput (last hour)", fill=(124, 45, 18), font=font(13, True))
    # pipeline strip
    nodes = ["Kafka", "Spark", "S3", "Dashboard"]
    nx = x1 + 80
    for node in nodes:
        rounded_rect(draw, (nx, y2 - 56, nx + 140, y2 - 16), 8, (254, 243, 199), (251, 191, 36))
        draw.text((nx + 28, y2 - 44), node, fill=(146, 64, 14), font=font(12, True))
        if node != nodes[-1]:
            draw.line((nx + 150, y2 - 36, nx + 190, y2 - 36), fill=(251, 191, 36), width=2)
        nx += 220
    save(img, "streaming")


def mock_kafka():
    img, draw, body = chrome("Kafka Streams Examples", (194, 65, 12))
    x1, y1, x2, y2 = body
    draw.text((x1 + 24, y1 + 20), "Event pipeline topology", fill=(124, 45, 18), font=font(18, True))
    boxes = [
        (x1 + 40, y1 + 80, "Producer"),
        (x1 + 280, y1 + 80, "Stream Processor"),
        (x1 + 520, y1 + 80, "Window Agg"),
        (x1 + 760, y1 + 80, "Sink / S3"),
    ]
    for bx, by, label in boxes:
        rounded_rect(draw, (bx, by, bx + 180, by + 70), 10, (255, 237, 213), (251, 146, 60))
        draw.text((bx + 24, by + 26), label, fill=(124, 45, 18), font=font(13, True))
    for i in range(3):
        x_start = x1 + 220 + i * 240
        draw.line((x_start, y1 + 115, x_start + 60, y1 + 115), fill=(234, 88, 12), width=3)
        draw.polygon([(x_start + 60, y1 + 115), (x_start + 50, y1 + 108), (x_start + 50, y1 + 122)], fill=(234, 88, 12))
    rounded_rect(draw, (x1 + 24, y1 + 200, x2 - 24, y2 - 24), 12, (15, 23, 42))
    log = (
        "[12:01:04] topic=orders partition=3 offset=1849201\n"
        "[12:01:04] window=5m count=12,441 avg_latency=42ms\n"
        "[12:01:05] checkpoint saved | lag=0 | consumers=4\n"
        "[12:01:05] output → s3://stream-bucket/agg/2026/06/16/"
    )
    draw.multiline_text((x1 + 44, y1 + 230), log, fill=(251, 191, 36), font=font(13), spacing=8)
    save(img, "kafka-streams")


def mock_airflow():
    img, draw, body = chrome("Airflow Data Pipelines", (22, 163, 74))
    x1, y1, x2, y2 = body
    tasks = [
        (x1 + 80, y1 + 100, "extract_s3"),
        (x1 + 320, y1 + 100, "validate"),
        (x1 + 560, y1 + 100, "transform"),
        (x1 + 800, y1 + 100, "load_warehouse"),
        (x1 + 320, y1 + 260, "notify_slack"),
    ]
    for tx, ty, name in tasks:
        color = (220, 252, 231) if name != "notify_slack" else (254, 249, 195)
        rounded_rect(draw, (tx, ty, tx + 160, ty + 56), 10, color, (134, 239, 172))
        draw.text((tx + 16, ty + 18), name, fill=(22, 101, 52), font=font(12, True))
    edges = [(0, 1), (1, 2), (2, 3), (2, 4)]
    coords = [(t[0] + 80, t[1] + 28) for t in tasks]
    for a, b in edges:
        draw.line((coords[a][0] + 80, coords[a][1], coords[b][0], coords[b][1]), fill=(34, 197, 94), width=2)
    rounded_rect(draw, (x1 + 24, y2 - 120, x2 - 24, y2 - 24), 10, (240, 253, 244))
    draw.text((x1 + 40, y2 - 100), "Last run: SUCCESS  •  SLA 98.2%  •  Duration 4m 12s  •  Retries 0", fill=(22, 101, 52), font=font(13))
    save(img, "airflow")


def mock_azure():
    img, draw, body = chrome("Azure Data Factory ETL", (37, 99, 235))
    x1, y1, x2, y2 = body
    sources = ["Blob Storage", "SQL DB", "REST API"]
    for i, s in enumerate(sources):
        rounded_rect(draw, (x1 + 40, y1 + 60 + i * 90, x1 + 220, y1 + 120 + i * 90), 10, (239, 246, 255), (147, 197, 253))
        draw.text((x1 + 60, y1 + 82 + i * 90), s, fill=(30, 64, 175), font=font(13))
        draw.line((x1 + 220, y1 + 90 + i * 90, x1 + 380, y1 + 200), fill=(59, 130, 246), width=2)
    rounded_rect(draw, (x1 + 380, y1 + 160, x1 + 620, y1 + 260), 14, (219, 234, 254), (96, 165, 250))
    draw.text((x1 + 420, y1 + 198), "ADF Pipeline", fill=(30, 64, 175), font=font(16, True))
    draw.line((x1 + 620, y1 + 210, x1 + 780, y1 + 210), fill=(59, 130, 246), width=2)
    rounded_rect(draw, (x1 + 780, y1 + 170, x2 - 40, y1 + 250), 10, (239, 246, 255), (147, 197, 253))
    draw.text((x1 + 800, y1 + 198), "Synapse / DW", fill=(30, 64, 175), font=font(14, True))
    rounded_rect(draw, (x1 + 24, y2 - 100, x2 - 24, y2 - 24), 10, (248, 250, 252))
    draw.text((x1 + 40, y2 - 78), "Runs today: 24  •  Failed: 0  •  Avg duration 6m  •  Data moved 18.4 GB", fill=(51, 65, 85), font=font(13))
    save(img, "azure-etl")


def mock_pyspark():
    img, draw, body = chrome("PySpark Processing Jobs", (180, 83, 9))
    x1, y1, x2, y2 = body
    rounded_rect(draw, (x1 + 24, y1 + 20, x2 - 24, y1 + 100), 10, (254, 243, 199))
    draw.text((x1 + 40, y1 + 38), "Job: customer_360_aggregate", fill=(146, 64, 14), font=font(16, True))
    draw.text((x1 + 40, y1 + 68), "Input: 102 GB  •  Stages: 14  •  Runtime: 8m 22s (-62%)", fill=(180, 83, 9), font=font(12))
    metrics = [("Executors", "8"), ("Partitions", "256"), ("Shuffle Read", "41 GB"), ("Spill", "0 B")]
    for i, (k, v) in enumerate(metrics):
        bx = x1 + 24 + i * 270
        rounded_rect(draw, (bx, y1 + 120, bx + 250, y1 + 190), 10, (255, 255, 255), (253, 230, 138))
        draw.text((bx + 16, y1 + 136), k, fill=(161, 98, 7), font=font(11))
        draw.text((bx + 16, y1 + 156), v, fill=(146, 64, 14), font=font(20, True))
    rounded_rect(draw, (x1 + 24, y1 + 210, x2 - 24, y2 - 24), 10, (15, 23, 42))
    spark_log = (
        "Stage 12/14 finished in 42s\n"
        "Broadcast join applied on dim_customers (12MB)\n"
        "Adaptive skew handling: merged 3 partitions\n"
        "Output written to s3://datalake/curated/customer_360/"
    )
    draw.multiline_text((x1 + 44, y1 + 240), spark_log, fill=(253, 230, 138), font=font(13), spacing=8)
    save(img, "pyspark")


def mock_analytics():
    img, draw, body = chrome("Analytics Dashboard", (109, 40, 217))
    x1, y1, x2, y2 = body
    kpis = [("Revenue", "$2.4M"), ("Users", "18.2K"), ("Conv.", "4.7%"), ("NPS", "62")]
    for i, (k, v) in enumerate(kpis):
        bx = x1 + 20 + i * 270
        rounded_rect(draw, (bx, y1 + 20, bx + 250, y1 + 90), 10, (245, 243, 255), (196, 181, 253))
        draw.text((bx + 16, y1 + 32), k, fill=(91, 33, 182), font=font(11))
        draw.text((bx + 16, y1 + 50), v, fill=(76, 29, 149), font=font(22, True))
    # bar chart
    rounded_rect(draw, (x1 + 20, y1 + 110, x1 + 620, y2 - 24), 12, (255, 255, 255), (221, 214, 254))
    draw.text((x1 + 36, y1 + 126), "Weekly signups by channel", fill=(76, 29, 149), font=font(14, True))
    bars = [120, 180, 95, 210, 160, 140, 190]
    for i, h in enumerate(bars):
        bx = x1 + 60 + i * 70
        draw.rounded_rectangle((bx, y2 - 40 - h, bx + 40, y2 - 50), radius=4, fill=(167, 139, 250))
    # donut
    rounded_rect(draw, (x1 + 640, y1 + 110, x2 - 20, y2 - 24), 12, (255, 255, 255), (221, 214, 254))
    cx, cy, r = x1 + 860, y1 + 280, 90
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(167, 139, 250), width=18)
    draw.text((cx - 30, cy - 10), "62%", fill=(76, 29, 149), font=font(20, True))
    draw.text((x1 + 660, y1 + 126), "Retention", fill=(76, 29, 149), font=font(14, True))
    save(img, "analytics")


def mock_forecasting():
    img, draw, body = chrome("Financial Forecasting", (8, 145, 178))
    x1, y1, x2, y2 = body
    draw.text((x1 + 24, y1 + 20), "Revenue forecast — next 6 months", fill=(22, 78, 99), font=font(16, True))
    pts_act, pts_fc = [], []
    for i in range(8):
        px = x1 + 60 + i * 120
        pts_act.append((px, y1 + 280 - i * 18))
    for i in range(6):
        px = x1 + 60 + (8 + i) * 120
        pts_fc.append((px, y1 + 200 - i * 22))
    draw.line(pts_act, fill=(14, 165, 233), width=3)
    draw.line(pts_fc, fill=(56, 189, 248), width=3)
    for p in pts_fc:
        draw.line((p[0], p[1], p[0], p[1] + 40), fill=(125, 211, 252), width=1)
    draw.text((x1 + 24, y2 - 70), "Model: XGBoost  •  MAPE 6.2%  •  CI 95%", fill=(8, 145, 178), font=font(13))
    save(img, "forecasting")


def mock_recommendation():
    img, draw, body = chrome("Recommendation System", (126, 34, 206))
    x1, y1, x2, y2 = body
    draw.text((x1 + 24, y1 + 20), "Recommended for you", fill=(88, 28, 135), font=font(18, True))
    items = [("Data Engineering Handbook", "92% match"), ("Kafka in Action", "88% match"), ("ML System Design", "85% match")]
    for i, (title, score) in enumerate(items):
        rounded_rect(draw, (x1 + 24, y1 + 70 + i * 100, x2 - 24, y1 + 150 + i * 100), 12, (250, 245, 255), (233, 213, 255))
        draw.text((x1 + 44, y1 + 92 + i * 100), title, fill=(88, 28, 135), font=font(14, True))
        draw.text((x2 - 140, y1 + 94 + i * 100), score, fill=(168, 85, 247), font=font(12, True))
    save(img, "recommendation")


def mock_sentiment():
    img, draw, body = chrome("Sentiment Analysis", (190, 24, 93))
    x1, y1, x2, y2 = body
    reviews = [
        ("\"Great product, fast delivery!\"", "Positive", (34, 197, 94)),
        ("\"Average experience, slow support.\"", "Neutral", (234, 179, 8)),
        ("\"Not worth the price.\"", "Negative", (239, 68, 68)),
    ]
    for i, (text, label, color) in enumerate(reviews):
        rounded_rect(draw, (x1 + 24, y1 + 30 + i * 110, x2 - 24, y1 + 120 + i * 110), 12, (255, 241, 246), (251, 207, 232))
        draw.text((x1 + 44, y1 + 52 + i * 110), text, fill=(131, 24, 67), font=font(13))
        rounded_rect(draw, (x2 - 160, y1 + 50 + i * 110, x2 - 44, y1 + 82 + i * 110), 8, color)
        draw.text((x2 - 148, y1 + 58 + i * 110), label, fill=(255, 255, 255), font=font(11, True))
    save(img, "sentiment")


def mock_scraping():
    img, draw, body = chrome("Web Scraping Pipeline", (71, 85, 105))
    x1, y1, x2, y2 = body
    steps = ["Fetch URLs", "Parse HTML", "Validate", "Dedupe", "Load PG"]
    for i, step in enumerate(steps):
        bx = x1 + 40 + i * 210
        rounded_rect(draw, (bx, y1 + 120, bx + 170, y1 + 180), 10, (241, 245, 249), (148, 163, 184))
        draw.text((bx + 20, y1 + 144), step, fill=(51, 65, 85), font=font(12, True))
        if i < len(steps) - 1:
            draw.line((bx + 175, y1 + 150, bx + 210, y1 + 150), fill=(100, 116, 139), width=2)
    rounded_rect(draw, (x1 + 24, y2 - 140, x2 - 24, y2 - 24), 10, (15, 23, 42))
    draw.multiline_text(
        (x1 + 44, y2 - 120),
        "Batch complete: 12,840 records ingested\nDuplicates removed: 312  •  Validation errors: 18\nPostgreSQL public.listings updated",
        fill=(203, 213, 225),
        font=font(13),
        spacing=6,
    )
    save(img, "web-scraping")


def mock_graph():
    img, draw, body = chrome("Graph ML Fraud Detection", (185, 28, 28))
    x1, y1, x2, y2 = body
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 - 20
    nodes = [(cx, cy - 120), (cx - 140, cy), (cx + 140, cy), (cx - 90, cy + 120), (cx + 90, cy + 120)]
    for i, n in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            draw.line((*n, *nodes[j]), fill=(254, 202, 202), width=2)
    for i, (nx, ny) in enumerate(nodes):
        color = (239, 68, 68) if i == 0 else (254, 226, 226)
        draw.ellipse((nx - 28, ny - 28, nx + 28, ny + 28), fill=color, outline=(220, 38, 38))
    draw.text((cx - 70, cy - 132), "Flagged", fill=(185, 28, 28), font=font(11, True))
    rounded_rect(draw, (x1 + 24, y2 - 80, x2 - 24, y2 - 24), 8, (254, 242, 242))
    draw.text((x1 + 40, y2 - 62), "Fraud score: 0.94  •  Network features: 27  •  Precision@k: 0.89", fill=(185, 28, 28), font=font(12))
    save(img, "graph-fraud")


def mock_deep_o_meter():
    img, draw, body = chrome("Deep-O-Meter — Deepfake Detection", (15, 23, 42))
    x1, y1, x2, y2 = body
    rounded_rect(draw, (x1 + 24, y1 + 24, x1 + 420, y2 - 24), 12, (30, 41, 59), (71, 85, 105))
    draw.text((x1 + 44, y1 + 44), "Upload media", fill=(226, 232, 240), font=font(14, True))
    draw.rounded_rectangle((x1 + 44, y1 + 80, x1 + 400, y1 + 280), radius=10, outline=(100, 116, 139), width=2)
    draw.text((x1 + 150, y1 + 170), "video.mp4", fill=(148, 163, 184), font=font(13))
    rounded_rect(draw, (x1 + 450, y1 + 24, x2 - 24, y2 - 24), 12, (248, 250, 252))
    draw.text((x1 + 470, y1 + 44), "Inference result", fill=(15, 23, 42), font=font(16, True))
    draw.text((x1 + 470, y1 + 90), "Prediction: SYNTHETIC", fill=(220, 38, 38), font=font(24, True))
    draw.text((x1 + 470, y1 + 140), "Confidence: 97.3%", fill=(51, 65, 85), font=font(14))
    draw.text((x1 + 470, y1 + 180), "Latency: 378ms  •  Model: v2.4 (MLflow)", fill=(100, 116, 139), font=font(12))
    save(img, "deep-o-meter")


def main() -> None:
    mock_chat_sql()
    mock_rag()
    mock_streaming()
    mock_kafka()
    mock_airflow()
    mock_azure()
    mock_pyspark()
    mock_analytics()
    mock_forecasting()
    mock_recommendation()
    mock_sentiment()
    mock_scraping()
    mock_graph()
    mock_deep_o_meter()


if __name__ == "__main__":
    main()
