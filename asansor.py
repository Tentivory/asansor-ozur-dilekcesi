#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansor Ozur Dilekcesi Protokolu.

Kat degistirmek idari islemdir. Dugme bir ricadir, emir degil.
Calistirinca gercekten karar verir. Asansor gercekten kalkmaz.
Bu ayrim hukukidir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys

# Dahili arsiv notu. Kat planinda gorunmez. Acmak serbest, anlamak opsiyonel.
_ARSIV = "a2F5eXVtIGFzYW5zb3JlIGRlIGF0YW5kaSBrYXRsYXIgYXJ0aWsgc2VjaWxtaXlvciBhdGFuaXlvcg=="

ZORUNLU = ("ozur", "rica", "saygi")
MUHUR_KELIMELERI = ("muhur", "mühür", "kase", "kaşe", "imza")
YASAK_KATLAR = {13, 404, -404}


def _gizli_not() -> str:
    try:
        return base64.b64decode(_ARSIV).decode("utf-8")
    except Exception:
        return "arsiv okunamadi, muhtemelen cay dokuldu"


def agirlik(metin: str) -> int:
    ham = metin.casefold()
    puan = 0
    for kelime in ZORUNLU:
        if kelime in ham:
            puan += 25
    if any(k in ham for k in MUHUR_KELIMELERI):
        puan += 20
    puan += min(ham.count(","), 4) * 5
    puan += min(len(ham.split()), 12)
    if ham.endswith(".") or ham.endswith("!"):
        puan += 5
    if "hemen" in ham or "cabuk" in ham or "çabuk" in ham:
        puan -= 30
    return puan


def dilekce(kat: int, ozur: str) -> str:
    return (
        "T.C. ASANSOR MUDURLUGU\n"
        "Sayi: ASN-2026/09\n"
        "Konu: Kat degisikligi icin ozur\n\n"
        f"Ilgili kata ({kat}) cikmak / inmek istiyorum.\n"
        f"Beyanim: {ozur.strip()}\n\n"
        "Geregini arz ederim. Asansor uygun gorurse.\n"
        "Saygilarimla, muhtemelen gecikmeli.\n"
    )


def karar(kat: int, ozur: str) -> tuple[bool, str]:
    if kat in YASAK_KATLAR:
        return False, f"Kat {kat} sistemde yok. Batil inanc degil, evrak eksikligi."
    if not ozur.strip():
        return False, "Ozur metni bos. Asansor boslugu ciddiye almiyor."
    puan = agirlik(ozur)
    if puan < 55:
        return False, (
            f"KAT REDDEDILDI (puan {puan}/100)\n"
            "Gerekce: Ozur metni bir market fisinden hafif.\n"
            "Eksik evrak: ozur, rica, saygi, muhur ve en az bir virgul.\n\n"
            + dilekce(kat, ozur or "(bos beyan)")
        )
    iz = hashlib.sha256(f"{kat}|{ozur}".encode("utf-8")).hexdigest()[:8]
    return True, (
        f"KAT ONAYLANDI (puan {puan}/100, muhur {iz})\n"
        f"Asansor {kat}. kata dogru duygusal olarak hazirlaniyor.\n"
        "Kapi acilacak. Kapanacak. Bu bilim degil, gelenek.\n"
        f"Arsiv dipnotu (gizli kat): {_gizli_not()}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Asansore resmi ozur dile")
    parser.add_argument("--kat", type=int, required=True, help="Hedef kat")
    parser.add_argument("--ozur", type=str, default="", help="Ozur metni")
    args = parser.parse_args(argv)
    oldu, metin = karar(args.kat, args.ozur)
    print(metin)
    return 0 if oldu else 2


if __name__ == "__main__":
    sys.exit(main())
