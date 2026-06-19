"""Copy personal photos into public/assets for portfolio sections."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(
    r"C:\Users\SRIVARDHANBABAVEMULA\.cursor\projects"
    r"\e-cinematic-portfolio-cinematic-portfolio-cinematic-portfolio-main\assets"
)
OUT = ROOT / "public" / "assets"

# destination -> source filename suffix (unique match in assets folder)
MAP = {
    "hero-foreground.png": "Gemini_Generated_Image___3_-69bdb6a0-4730-42a7-a798-895071495a5a.png",
    "hero1.png": "Gemini_Generated_Image___3_-69bdb6a0-4730-42a7-a798-895071495a5a.png",
    "photo-casual.png": "WhatsApp_Image_2026-06-16_at_1.42.09_PM__2_-f6dd4039-ceaf-4561-aafa-4ffd9a430af1.png",
    "photo-bw-dramatic.png": "IMG-20250926-WA0012__1_.jpg-cff76224-9163-41ec-9a69-0628d8a6730d.png",
    "photo-campus-night.png": "CAMPUS__16_-3e1ea21b-5b02-4d31-9f06-fc8e8d2eef23.png",
    "photo-campus-wide.png": "CAMPUS__9_-bab04615-086d-4676-b317-fc52c6251257.png",
    "srivardhan-about.png": "IMG-20250926-WA0013.jpg-1def63aa-ecf0-46a4-a26e-1f70664c94a9.png",
    "work-experience.png": "IMG-20250926-WA0012__1_.jpg-cff76224-9163-41ec-9a69-0628d8a6730d.png",
    "photo-office-1.png": "WhatsApp_Image_2026-06-16_at_1.42.08_PM-c611ec64-7d0e-412a-9cb7-c277746f596b.png",
    "photo-office-2.png": "WhatsApp_Image_2026-06-16_at_1.42.09_PM-8e147b08-38f4-4a05-89d5-d082e6afa5ac.png",
    "photo-office-3.png": "WhatsApp_Image_2026-06-16_at_1.42.08_PM__4_-ee0838da-ab1d-49b8-bd09-4d26e4b1eac8.png",
    "photo-portrait.png": "WhatsApp_Image_2026-06-16_at_1.42.09_PM__4_-2572e465-3ae3-41f8-96e8-0a3b3e9c0550.png",
    "photo-campus-1.png": "CAMPUS__9_-15960027-024c-4ac4-89a0-2269b8435a21.png",
    "photo-campus-2.png": "CAMPUS__6_-d15e90db-6b92-4e84-9ce8-7f5e3a015621.png",
    "photo-campus-3.png": "CAMPUS__16_-91660436-ef41-4186-a33a-e4418aea1150.png",
    "photo-campus-4.png": "IMG-20260126-WA0007.jpg-93cf05fd-aea6-489b-9903-90bac7fad9e7.png",
    "photo-campus-5.png": "IMG-20260126-WA0009.jpg-8db625f4-537b-4cb0-bfff-eee9b6bc2d3c.png",
    "intro-slide-1.png": "WhatsApp_Image_2026-06-16_at_1.42.08_PM-c611ec64-7d0e-412a-9cb7-c277746f596b.png",
    "intro-slide-2.png": "IMG-20250926-WA0013.jpg-1def63aa-ecf0-46a4-a26e-1f70664c94a9.png",
    "intro-slide-3.png": "IMG-20250926-WA0012__1_.jpg-951e91d3-6850-4936-aed3-327e441baf6d.png",
    "intro-slide-4.png": "CAMPUS__9_-15960027-024c-4ac4-89a0-2269b8435a21.png",
}


def find_source(suffix: str) -> Path | None:
    matches = list(SRC.glob(f"*{suffix}"))
    return matches[0] if matches else None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for dst, suffix in MAP.items():
        src = find_source(suffix)
        if not src:
            print(f"MISSING source for {dst} ({suffix})")
            continue
        target = OUT / dst
        shutil.copy2(src, target)
        print(f"Copied {src.name} -> {dst}")


if __name__ == "__main__":
    main()
