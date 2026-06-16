"""Split certificate PDF into per-page PNG images for modal previews."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymupdf', '-q'])
    import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public' / 'assets' / 'certs'

SOURCES = [
    Path(r'c:\Users\SRIVARDHANBABAVEMULA\Downloads\CERTIFICATE OF SKILLS ---1.pdf'),
    ROOT / 'public' / 'assets' / 'certificate-of-skills.pdf',
]


def main() -> None:
    src = next((p for p in SOURCES if p.exists()), None)
    if not src:
        raise SystemExit('Certificate PDF not found')

    OUT.mkdir(parents=True, exist_ok=True)
    dest_pdf = ROOT / 'public' / 'assets' / 'certificate-of-skills.pdf'
    if src.resolve() != dest_pdf.resolve():
        shutil.copy2(src, dest_pdf)

    doc = fitz.open(src)
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        out_path = OUT / f'cert-{i + 1:02d}.png'
        pix.save(str(out_path))
        print(f'Page {i + 1}: {out_path.name} ({pix.width}x{pix.height})')
    doc.close()
    print(f'Done — {len(list(OUT.glob("*.png")))} images in {OUT}')


if __name__ == '__main__':
    main()
