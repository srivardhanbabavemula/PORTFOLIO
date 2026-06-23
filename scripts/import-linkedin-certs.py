"""Import LinkedIn Learning certificate PDFs as PNG previews and rebuild profile publications."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
    import fitz

ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = Path(
    r"C:\Users\SRIVARDHANBABAVEMULA\Downloads\Fwd_ Certification of courses learned and pay slips"
)
OUT = ROOT / "public" / "assets" / "certs"
PROFILE = ROOT / "data" / "profile.json"

# Keep IBM / Coursera / Infosys entries — images already at cert-01 … cert-13
LEGACY_CERTS = [
    {
        "title": "IBM Data Science Professional Certificate",
        "platform": "IBM · Coursera",
        "year": "Oct 2022",
        "certImage": "/assets/certs/cert-01.png",
        "link": "https://coursera.org/verify/professional-cert/6SS3RUJSD6SZ",
        "desc": "10-course professional certificate: Python, SQL, ML, visualization, and capstone.",
    },
    {
        "title": "IBM Data Analyst Professional Certificate",
        "platform": "IBM · Coursera",
        "year": "May 2023",
        "certImage": "/assets/certs/cert-02.png",
        "link": "https://coursera.org/verify/professional-cert/KQUJBR5S8XAB",
        "desc": "9-course certificate in Excel, SQL, Python, Cognos Analytics, and data analysis.",
    },
    {
        "title": "Data Analysis & Visualization Foundations",
        "platform": "IBM · Coursera",
        "year": "May 2023",
        "certImage": "/assets/certs/cert-03.png",
        "link": "https://coursera.org/verify/specialization/2ZJ44UX7ASYQ",
        "desc": "Excel, data visualization, pivot tables, and IBM Cognos Analytics dashboards.",
    },
    {
        "title": "Google Crash Course on Python",
        "platform": "Google · Coursera",
        "year": "Apr 2022",
        "certImage": "/assets/certs/cert-04.png",
        "link": "https://coursera.org/verify/5BHT82QXNJXB",
        "desc": "Python fundamentals, data structures, and problem-solving.",
    },
    {
        "title": "Infosys Young Python Professional",
        "platform": "Infosys",
        "year": "Sep 2023",
        "certImage": "/assets/certs/cert-05.png",
        "link": "https://verify.onwingspan.com",
        "desc": "Advanced Python professional program via Infosys Springboard.",
    },
    {
        "title": "Programming Fundamentals using Python — Part 1",
        "platform": "Infosys",
        "year": "Aug 2023",
        "certImage": "/assets/certs/cert-06.png",
        "link": "https://verify.onwingspan.com",
        "desc": "Core Python programming fundamentals and problem solving.",
    },
    {
        "title": "Programming Fundamentals using Python — Part 2",
        "platform": "Infosys",
        "year": "Sep 2023",
        "certImage": "/assets/certs/cert-07.png",
        "link": "https://verify.onwingspan.com",
        "desc": "Advanced Python programming concepts and application development.",
    },
    {
        "title": "Object-Oriented Programming using Python",
        "platform": "Infosys",
        "year": "Sep 2023",
        "certImage": "/assets/certs/cert-08.png",
        "link": "https://verify.onwingspan.com",
        "desc": "OOP principles, class design, and Python software patterns.",
    },
    {
        "title": "SQL & Relational Database 101",
        "platform": "IBM Cognitive Class",
        "year": "Mar 2022",
        "certImage": "/assets/certs/cert-09.png",
        "link": "https://courses.cognitiveclass.ai/certificates/a08d9f1fbc9c47bb8fe3610f18a580c5",
        "desc": "Relational database design, SQL querying, and data modeling.",
    },
    {
        "title": "Keys & Constraints in MySQL",
        "platform": "IBM Cognitive Class",
        "year": "Mar 2022",
        "certImage": "/assets/certs/cert-10.png",
        "link": "https://courses.cognitiveclass.ai/certificates/7e591e47c2424acb8b433ab9067eff88",
        "desc": "Primary keys, foreign keys, and MySQL schema constraints.",
    },
    {
        "title": "Create Tables & Load Data in MySQL",
        "platform": "IBM Cognitive Class",
        "year": "Mar 2022",
        "certImage": "/assets/certs/cert-11.png",
        "link": "https://courses.cognitiveclass.ai/certificates/8e1738e25e2844dca124a4ea102a733b",
        "desc": "MySQL table creation and data loading with phpMyAdmin.",
    },
    {
        "title": "Views in PostgreSQL",
        "platform": "IBM Cognitive Class",
        "year": "Mar 2022",
        "certImage": "/assets/certs/cert-12.png",
        "link": "https://courses.cognitiveclass.ai/certificates/16c6e3da46954ddfaade76e46660b5e2",
        "desc": "PostgreSQL views and database management.",
    },
    {
        "title": "Spark Fundamentals I",
        "platform": "Big Data University",
        "year": "Mar 2022",
        "certImage": "/assets/certs/cert-13.png",
        "link": "https://courses.cognitiveclass.ai/certificates/4537607578e147a2ab76a405cd6d5194",
        "desc": "Apache Spark architecture, RDDs, and distributed processing.",
    },
]

LINKEDIN = "https://www.linkedin.com/in/srivardhan-baba-vemula/details/certifications/"


def norm_key(filename: str) -> str:
    base = filename.replace("CertificateOfCompletion_", "").replace(".pdf", "")
    return re.sub(r"\s+\(\d+\)$", "", base).strip()


def pick_best(files: list[Path]) -> Path:
    def score(p: Path) -> tuple[int, str]:
        m = re.search(r"\((\d+)\)\.pdf$", p.name)
        return (0 if not m else int(m.group(1)), p.name)

    no_paren = [p for p in files if not re.search(r"\(\d+\)\.pdf$", p.name)]
    if no_paren:
        return sorted(no_paren, key=lambda p: p.name)[0]
    return sorted(files, key=score)[0]


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


def title_from_key(key: str) -> str:
    return key.replace("  ", " ").strip()


def pdf_to_png(pdf: Path, out: Path) -> None:
    doc = fitz.open(pdf)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    pix.save(str(out))
    doc.close()


def platform_for(title: str) -> str:
    t = title.lower()
    if "microsoft" in t or "azure" in t or "copilot" in t or "power platform" in t or "windows" in t:
        return "Microsoft · LinkedIn Learning"
    if "aws" in t:
        return "AWS · LinkedIn Learning"
    if "career essentials" in t:
        return "Microsoft & LinkedIn"
    if "openai" in t or "langchain" in t:
        return "LinkedIn Learning"
    return "LinkedIn Learning"


def main() -> None:
    if not CERT_DIR.is_dir():
        raise SystemExit(f"Certificate folder not found: {CERT_DIR}")

    OUT.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(CERT_DIR.glob("CertificateOfCompletion_*.pdf"))
    groups: dict[str, list[Path]] = {}
    for p in pdfs:
        groups.setdefault(norm_key(p.name), []).append(p)

    linkedin_entries = []
    for key in sorted(groups.keys()):
        pdf = pick_best(groups[key])
        slug = slugify(key)
        out_name = f"linkedin-{slug}.png"
        out_path = OUT / out_name
        pdf_to_png(pdf, out_path)
        title = title_from_key(key)
        linkedin_entries.append({
            "title": title,
            "platform": platform_for(title),
            "year": "2024",
            "certImage": f"/assets/certs/{out_name}",
            "link": LINKEDIN,
            "desc": f"LinkedIn Learning certificate of completion — {title}.",
        })
        print(f"  {out_name} <- {pdf.name}")

    publications = []
    for i, c in enumerate(LEGACY_CERTS, start=1):
        publications.append({"id": i, **c})
    for i, c in enumerate(linkedin_entries, start=len(LEGACY_CERTS) + 1):
        publications.append({"id": i, **c})

    data = json.loads(PROFILE.read_text(encoding="utf-8"))
    data["publications"] = publications

    for stat in data.get("stats", []):
        if "cert" in stat.get("label", "").lower():
            stat["value"] = str(len(publications))

    PROFILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nTotal certifications: {len(publications)} ({len(LEGACY_CERTS)} legacy + {len(linkedin_entries)} LinkedIn)")


if __name__ == "__main__":
    main()
