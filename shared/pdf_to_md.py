#!/usr/bin/env python3
"""Stufe 0: Convert <bank>/pdf/*.pdf to <bank>/.md/*.md using pymupdf4llm."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from pathlib import Path
import sys

import pymupdf4llm


def _convert_one(
    pdf_path_str: str,
    target_md_str: str,
    images_dir_str: str,
    write_images: bool,
    use_ocr: bool,
) -> tuple[str, bool, str]:
    pdf_path = Path(pdf_path_str)
    target_md = Path(target_md_str)
    images_dir = Path(images_dir_str)
    stem = pdf_path.stem
    try:
        kwargs: dict = {"use_ocr": use_ocr}
        if write_images:
            img_sub = images_dir / stem
            img_sub.mkdir(parents=True, exist_ok=True)
            kwargs.update(
                {
                    "write_images": True,
                    "image_path": str(img_sub),
                    "image_format": "png",
                }
            )
        else:
            kwargs["write_images"] = False

        md_text = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)
        if (not md_text or len(md_text.strip()) < 100) and not use_ocr:
            # Fallback to OCR if the PDF appears to be a pure scan
            kwargs["use_ocr"] = True
            md_text = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)

        if not md_text or not md_text.strip():
            return pdf_path.name, False, "empty markdown"

        if write_images:
            md_text = md_text.replace(f"{images_dir / stem}/", f"images/{stem}/")
            md_text = md_text.replace(f"{images_dir}/", "images/")
        target_md.write_text(md_text, encoding="utf-8")
        return pdf_path.name, True, f"{len(md_text):,} chars"
    except Exception as exc:
        return pdf_path.name, False, str(exc)


def convert_bank_pdfs(
    bank_dir: Path,
    *,
    force: bool = False,
    write_images: bool = False,
    use_ocr: bool = False,
    workers: int | None = None,
    limit: int | None = None,
    pattern: str = "*.pdf",
) -> tuple[int, int]:
    pdf_dir = bank_dir / "pdf"
    md_dir = bank_dir / ".md"
    images_dir = md_dir / "images"

    pdfs = sorted(pdf_dir.glob(pattern))
    if not pdfs:
        print(f"[WARN] No PDFs matching {pattern} in {pdf_dir}", flush=True)
        return 0, 0

    md_dir.mkdir(parents=True, exist_ok=True)
    todo: list[tuple[Path, Path]] = []
    ok = 0
    for pdf_path in pdfs:
        target_md = md_dir / f"{pdf_path.stem}.md"
        if target_md.exists() and target_md.stat().st_size > 0 and not force:
            ok += 1
        else:
            todo.append((pdf_path, target_md))

    todo.sort(key=lambda pair: pair[0].stat().st_size)
    if limit is not None and limit > 0:
        todo = todo[:limit]

    if todo:
        max_workers = workers or min(4, os.cpu_count() or 2)
        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(
                    _convert_one,
                    str(pdf_path),
                    str(target_md),
                    str(images_dir),
                    write_images,
                    use_ocr,
                ): pdf_path.name
                for pdf_path, target_md in todo
            }
            for idx, fut in enumerate(as_completed(futures), start=1):
                name, success, info = fut.result()
                if success:
                    ok += 1
                    print(f"[{idx}/{len(todo)}] [OK] {name} ({info})", flush=True)
                else:
                    print(f"[{idx}/{len(todo)}] [ERROR] {name}: {info}", flush=True)

    print(f"[DONE] {bank_dir.name}: {ok}/{len(pdfs)} PDFs converted to Markdown.", flush=True)
    return ok, len(pdfs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert bank PDFs to Markdown.")
    parser.add_argument("--bank", required=True, help="Bank directory (zkb, gekb, vskb, bcv)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .md files")
    parser.add_argument("--write-images", action="store_true", help="Extract PNG images")
    parser.add_argument("--use-ocr", action="store_true", help="Force OCR on every PDF")
    parser.add_argument("--workers", type=int, default=None, help="Parallel worker processes")
    parser.add_argument("--limit", type=int, default=None, help="Max PDFs to convert in this run")
    parser.add_argument("--pattern", default="*.pdf", help="Glob pattern inside <bank>/pdf/")
    args = parser.parse_args()

    bank_dir = Path(args.bank)
    if not bank_dir.is_dir():
        print(f"Bank directory not found: {bank_dir}", file=sys.stderr)
        sys.exit(1)

    ok, total = convert_bank_pdfs(
        bank_dir,
        force=args.force,
        write_images=args.write_images,
        use_ocr=args.use_ocr,
        workers=args.workers,
        limit=args.limit,
        pattern=args.pattern,
    )
    if total > 0 and ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
