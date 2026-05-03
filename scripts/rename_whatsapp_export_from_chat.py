#!/usr/bin/env python3
"""
Renomeia ficheiros da exportação WhatsApp (pasta com _chat.txt) usando o texto da
mensagem na mesma linha do <anexado: ...>. Mantém o prefixo numérico inicial
(ex.: 00000182-...) para os scripts do memorial continuarem a encontrar ficheiros.

Uso:
  python3 scripts/rename_whatsapp_export_from_chat.py [--dry-run] [CAMINHO_PASTA]

Por omissão usa «WhatsApp Chat - PONTE AMADEU» na raiz do repositório.
"""

from __future__ import annotations

import argparse
import os
import re
import unicodedata
from pathlib import Path

ANEX_RE = re.compile(r"<anexado:\s*([^>]+)>")
LINE_RE = re.compile(
    r"^(?:\u200e)?\[\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2}\]\s*([^:]+):\s*(.*)$"
)


def slugify(text: str, max_len: int = 90) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("\u200e", "").strip()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^0-9A-Za-z_.\-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return (text[:max_len].rstrip("._") or "sem_texto")


def file_prefix_and_ext(name: str) -> tuple[str, str]:
    m = re.match(r"^(-?\d{6,})-(.+)$", name)
    if not m:
        return "", Path(name).suffix.lower()
    rest = m.group(2)
    ext = Path(rest).suffix.lower()
    if ext in (".jpg", ".jpeg", ".png", ".pdf", ".docx"):
        return m.group(1), ext
    return m.group(1), Path(name).suffix.lower()


def build_caption_map(chat_path: Path) -> dict[str, str]:
    lines = chat_path.read_text(encoding="utf-8", errors="replace").splitlines()
    state = ""
    out: dict[str, str] = {}
    for line in lines:
        m = LINE_RE.match(line)
        if m:
            who, rest = m.group(1).strip(), m.group(2)
            if "Lindinha" in who and "<anexado:" not in rest:
                t = rest.replace("\u200e", "").strip()
                if t:
                    state = t
        am = ANEX_RE.search(line)
        if not am:
            continue
        fn = am.group(1).strip()
        body = ""
        if m := LINE_RE.match(line):
            body = m.group(2).split("<anexado:")[0].strip()
        body = body or state or "sem_legenda_na_linha"
        out[fn] = body
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "folder",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1] / "WhatsApp Chat - PONTE AMADEU"),
        help="Pasta da exportação (com _chat.txt)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Só mostrar, não renomear")
    args = ap.parse_args()
    folder = Path(args.folder)
    chat = folder / "_chat.txt"
    if not chat.is_file():
        raise SystemExit(f"Não encontrado: {chat}")

    cap_map = build_caption_map(chat)
    used: dict[str, int] = {}
    renamed = 0
    for name in sorted(os.listdir(folder)):
        path = folder / name
        if not path.is_file() or name == "_chat.txt":
            continue
        low = name.lower()
        if not low.endswith((".jpg", ".jpeg", ".png", ".pdf", ".docx")):
            continue
        prefix, ext = file_prefix_and_ext(name)
        if not prefix:
            continue
        cap = cap_map.get(name, "nao_listado_no_chat")
        slug = slugify(cap)
        base = f"{prefix}-{slug}"
        key = base.lower()
        used[key] = used.get(key, 0) + 1
        if used[key] > 1:
            base = f"{prefix}-{slug}_{used[key]}"
        new_name = base + ext
        if new_name == name:
            continue
        dest = folder / new_name
        if dest.exists():
            base = f"{prefix}-{slug}_dup{used[key]}"
            new_name = base + ext
            dest = folder / new_name
        print(f"{name} -> {new_name}")
        if not args.dry_run:
            path.rename(dest)
        renamed += 1
    print(f"Total: {renamed} ficheiros" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
