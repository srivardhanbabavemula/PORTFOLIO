"""Copy user-provided project banner images into public/assets/projects."""
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

# source filename fragment -> output filename
COVERS = {
    "ai-data-analyst-chatbot": "ai-chatbot.png",
    "rag-ai-document-qa": "rag-qa.png",
    "real-time-streaming": "streaming.png",
    "kafka-streams": "kafka-streams.png",
    "airflow-data-pipelines": "airflow.png",
    "azure-data-factory-etl": "azure-etl.png",
    "pyspark-processing": "pyspark.png",
    "analytics-dashboard": "analytics.png",
    "financial-forecasting": "forecasting.png",
    "recommendation-system": "recommendation.png",
    "sentiment-analysis": "sentiment.png",
    "web-scraping-pipeline": "web-scraping.png",
    "graph-ml-fraud": "graph-fraud.png",
    "enterprise-ai": "deep-o-meter.png",
}

# project title substring -> output filename (must match COVERS values)
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
    copied = {}

    for fragment, dst_name in COVERS.items():
        src = find_source(fragment)
        if not src:
            print(f"MISSING: {fragment}")
            continue
        target = OUT / dst_name
        shutil.copy2(src, target)
        copied[dst_name] = target
        print(f"Copied -> {dst_name}")

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
        path = f"/assets/projects/{fname}"
        proj["image"] = path
        # bgImage stays personal photos — do not overwrite with project banners

    PROFILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {len(data['projects'])} projects in profile.json")


if __name__ == "__main__":
    main()
