#!/usr/bin/env python3
"""
Copia `_chat.txt` completo e anexos com prefixo numérico > âncora a partir da pasta
export no Downloads, remove no repositório variantes antigas desses prefixos,
e renomeia só os ficheiros cujo nome ainda coincide com <anexado:...> no chat.

Âncora por omissão: 279 (mensagem «CORRIGIR» + 00000279-PHOTO-... = último ponto
considerado já correto no memorial; integrar tudo com prefixo > 279).

Uso:
  python3 scripts/sync_whatsapp_incremental_from_downloads.py [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ANEX_RE = re.compile(r"<anexado:\s*([^>]+)>")
PREFIX_RE = re.compile(r"^(\d{6,})-")

ROOT = Path(__file__).resolve().parents[1]
SRC_DEFAULT = Path.home() / "Downloads" / "WhatsApp Chat - PONTE AMADEU"
DST_DEFAULT = ROOT / "WhatsApp Chat - PONTE AMADEU"


def numeric_prefix(name: str) -> int | None:
    m = PREFIX_RE.match(name)
    if not m:
        return None
    return int(m.group(1))


def collect_attachments_after(chat_text: str, anchor: int) -> set[str]:
    out: set[str] = set()
    for m in ANEX_RE.finditer(chat_text):
        fn = m.group(1).strip()
        p = numeric_prefix(fn)
        if p is not None and p > anchor:
            out.add(fn)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=SRC_DEFAULT, help="Pasta export WhatsApp (Downloads)")
    ap.add_argument("--dest", type=Path, default=DST_DEFAULT, help="Pasta no repositório")
    ap.add_argument("--anchor", type=int, default=279, help="Não copiar nem apagar prefixos <= âncora")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    src: Path = args.source
    dst: Path = args.dest
    anchor: int = args.anchor

    schat = src / "_chat.txt"
    if not schat.is_file():
        raise SystemExit(f"Fonte sem _chat.txt: {schat}")
    dst.mkdir(parents=True, exist_ok=True)

    text = schat.read_text(encoding="utf-8", errors="replace")
    to_sync = collect_attachments_after(text, anchor)

    if args.dry_run:
        print(f"[dry-run] Copiaria _chat.txt de {src} -> {dst}")
    else:
        shutil.copy2(schat, dst / "_chat.txt")
        print(f"Atualizado: {dst / '_chat.txt'}")

    removed = 0
    for name in list(os.listdir(dst)):
        if name == "_chat.txt":
            continue
        path = dst / name
        if not path.is_file():
            continue
        p = numeric_prefix(name)
        if p is None or p <= anchor:
            continue
        if args.dry_run:
            print(f"[dry-run] removeria: {name}")
        else:
            path.unlink()
        removed += 1

    copied = 0
    missing: list[str] = []
    for fn in sorted(to_sync):
        sp = src / fn
        if not sp.is_file():
            missing.append(fn)
            continue
        if args.dry_run:
            print(f"[dry-run] copiaria: {fn}")
        else:
            shutil.copy2(sp, dst / fn)
        copied += 1

    print(
        f"Anexos no chat com prefixo > {anchor}: {len(to_sync)}; "
        f"copiados: {copied}; em falta na fonte: {len(missing)}; "
        f"removidos no destino (prefixo > {anchor}): {removed}"
    )
    if missing:
        print("Ficheiros referenciados no chat mas ausentes na pasta fonte:")
        for m in missing[:40]:
            print(f"  - {m}")
        if len(missing) > 40:
            print(f"  ... e mais {len(missing) - 40}")

    if args.dry_run:
        print("[dry-run] Não executar rename.")
        return

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "rename_whatsapp_export_from_chat.py"),
            str(dst),
            "--only-with-chat-key",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
