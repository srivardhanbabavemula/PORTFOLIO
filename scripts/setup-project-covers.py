"""Copy project banner images into public/assets/projects and update profile.json."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(
    r"C:\Users\SRIVARDHANBABAVEMULA\.cursor\projects"
    r"\e-cinematic-portfolio-cinematic-portfolio-cinematic-portfolio-main\assets"
)
OUT = ROOT / "public" / "assets" / "projects"
PROFILE = ROOT / "data" / "profile.json"

# fragment in source filename -> output filename (14 portfolio projects)
PROJECT_COVERS = {
    "ChatGPT_Image_Jun_25__2026__02_13_38_PM-3ca266f7": "ai-chatbot.png",
    "ChatGPT_Image_Jun_25__2026__02_13_04_PM-55588735": "rag-qa.png",
    "ChatGPT_Image_Jun_25__2026__02_13_45_PM-f5cefb9d": "streaming.png",
    "ChatGPT_Image_Jun_25__2026__02_13_41_PM-92506bef": "kafka-streams.png",
    "ChatGPT_Image_Jun_25__2026__02_13_39_PM-50bb242a": "airflow.png",
    "ChatGPT_Image_Jun_25__2026__02_13_40_PM-3e6efdf8": "azure-etl.png",
    "ChatGPT_Image_Jun_25__2026__02_13_43_PM-dcbdaef6": "pyspark.png",
    "ChatGPT_Image_Jun_25__2026__02_13_10_PM-8f2d6a9d": "analytics.png",
    "ChatGPT_Image_Jun_25__2026__02_13_17_PM-ff30e119": "forecasting.png",
    "recommendation-system-a383d243": "recommendation.png",
    "ChatGPT_Image_Jun_25__2026__02_13_14_PM-52f386af": "sentiment.png",
    "ChatGPT_Image_Jun_25__2026__02_13_46_PM-4c2fae24": "web-scraping.png",
    "ChatGPT_Image_Jun_25__2026__02_13_05_PM-9fdc27ca": "graph-fraud.png",
    "ChatGPT_Image_Jun_25__2026__02_13_07_PM-947d763f": "deep-o-meter.png",
}

TITLE_MAP = {
    "AI Data Analyst Chatbot": "ai-chatbot.png",
    "RAG Document Q&A": "rag-qa.png",
    "Real-Time Streaming": "streaming.png",
    "Kafka Streams": "kafka-streams.png",
    "Airflow Data Pipelines": "airflow.png",
    "Azure Data Factory ETL": "azure-etl.png",
    "PySpark Processing": "pyspark.png",
    "Analytics Dashboard": "analytics.png",
    "Financial Forecasting": "forecasting.png",
    "Recommendation System": "recommendation.png",
    "Sentiment Analysis": "sentiment.png",
    "Web Scraping Pipeline": "web-scraping.png",
    "Graph ML Fraud Detection": "graph-fraud.png",
    "Deep-O-Meter": "deep-o-meter.png",
}


def find_source(fragment: str) -> Path | None:
    matches = list(SRC.glob(f"*{fragment}*.png"))
    return matches[0] if matches else None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for fragment, dst_name in PROJECT_COVERS.items():
        src = find_source(fragment)
        if not src:
            print(f"MISSING: {fragment} -> {dst_name}")
            continue
        target = OUT / dst_name
        shutil.copy2(src, target)
        print(f"Copied {src.name[:48]}... -> {dst_name}")

    data = json.loads(PROFILE.read_text(encoding="utf-8"))
    for proj in data["projects"]:
        fname = None
        for key, name in TITLE_MAP.items():
            if key in proj["title"]:
                fname = name
                break
        if not fname:
            print(f"No mapping for: {proj['title']}")
            continue
        proj["image"] = f"/assets/projects/{fname}"

    PROFILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(data['projects'])} projects in profile.json")


if __name__ == "__main__":
    main()
