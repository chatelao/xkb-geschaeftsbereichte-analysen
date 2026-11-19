#!/usr/bin/env python3
"""Shared PDF download, integrity check, and manifest utilities."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def is_valid_pdf(data: bytes, min_bytes: int = 10_000) -> bool:
    if len(data) < min_bytes:
        return False
    if not data.lstrip().startswith(b"%PDF"):
        return False
    if b"%%EOF" not in data[-4096:]:
        return False
    return True


def download_pdf(
    url: str,
    target_path: Path,
    *,
    retries: int = 4,
    timeout: int = 45,
    force: bool = False,
) -> dict:
    """Download a PDF with integrity validation and exponential backoff."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and not force:
        existing = target_path.read_bytes()
        if is_valid_pdf(existing):
            return {
                "filename": target_path.name,
                "url": url,
                "status": "cached",
                "bytes": len(existing),
                "sha256": hashlib.sha256(existing).hexdigest(),
            }

    last_err = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
            if is_valid_pdf(data):
                target_path.write_bytes(data)
                return {
                    "filename": target_path.name,
                    "url": url,
                    "status": "downloaded",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            last_err = f"Invalid PDF (bytes={len(data)}, head={data[:16]!r})"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_err = str(exc)
        if attempt < retries - 1:
            time.sleep(2 ** attempt)

    return {
        "filename": target_path.name,
        "url": url,
        "status": "failed",
        "error": last_err,
    }


def download_catalog(
    catalog: dict[str, str | list[str]],
    pdf_dir: Path,
    *,
    force: bool = False,
    sleep_sec: float = 0.25,
) -> list[dict]:
    """Download all PDFs in {filename: url_or_urls} into pdf_dir and write pdf_manifest.json."""
    pdf_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    items = sorted(catalog.items())
    for idx, (filename, urls) in enumerate(items, start=1):
        url_list = [urls] if isinstance(urls, str) else list(urls)
        target = pdf_dir / filename
        res: dict = {"filename": filename, "status": "failed", "error": "no urls"}
        for url in url_list:
            res = download_pdf(url, target, force=force)
            if res["status"] in {"downloaded", "cached"}:
                break
        if res["status"] == "downloaded":
            print(f"[{idx}/{len(items)}] [OK] {filename} ({res['bytes']:,} B)")
            time.sleep(sleep_sec)
        elif res["status"] == "cached":
            print(f"[{idx}/{len(items)}] [SKIP] {filename} (cached)")
        else:
            print(f"[{idx}/{len(items)}] [FAIL] {filename}: {res.get('error')}")
        results.append(res)

    manifest_path = pdf_dir.parent / "pdf_manifest.json"
    manifest_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    ok = sum(1 for r in results if r["status"] in {"downloaded", "cached"})
    print(f"Summary for {pdf_dir}: {ok}/{len(results)} PDFs available.")
    return results
