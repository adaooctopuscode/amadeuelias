#!/usr/bin/env python3
"""
Renumera apenas o prefixo «Figura N:» nas legendas, na ordem de aparição
no documento (1, 2, 3, …). Não altera texto da legenda após os dois pontos.
"""
from __future__ import annotations

import os
import re
import sys

from docx import Document

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC_PATH = os.path.join(ROOT, "MC-AMADEU ELIAS R0.docx")

CAPTION = re.compile(r"^\s*Figura\s+\d+\s*:\s*(.*)$", re.DOTALL)


def main() -> None:
    doc = Document(DOC_PATH)
    n = 0
    for para in doc.paragraphs:
        m = CAPTION.match(para.text)
        if not m:
            continue
        n += 1
        body = m.group(1)
        para.text = f"Figura {n}: {body}"
    if n == 0:
        print("ERRO: nenhuma legenda «Figura N:» encontrada.", file=sys.stderr)
        raise SystemExit(1)
    doc.save(DOC_PATH)
    print(f"OK: {n} legendas renumeradas (Figura 1 … Figura{n}).")
    print("Gravado:", DOC_PATH)


if __name__ == "__main__":
    main()
