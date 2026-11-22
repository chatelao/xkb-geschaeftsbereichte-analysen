#!/usr/bin/env python3
"""Phase 9: Bereitet `.rtd_docs/` für MkDocs Material / Read the Docs / GitHub Pages vor."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from shared.config import REPO_ROOT, VALID_BANKS, load_bank_config

RTD_DIR = REPO_ROOT / ".rtd_docs"
GH_BLOB = "https://github.com/chatelao/xkb-geschaeftsbereichte-analysen/blob/main"
GH_TREE = "https://github.com/chatelao/xkb-geschaeftsbereichte-analysen/tree/main"


def _rewrite_github_links(text: str, rel_dir: str = "") -> str:
    prefix = f"{rel_dir}/" if rel_dir else ""
    text = re.sub(r"\(\./([a-zA-Z0-9_/-]+\.(?:py|json|yaml|yml|csv))\)", rf"({GH_BLOB}/{prefix}\1)", text)
    text = re.sub(r"\(\./(shared|tests|pdf|\.md)/?\)", rf"({GH_TREE}/{prefix}\1)", text)
    return text


def prepare_docs() -> Path:
    if RTD_DIR.exists():
        shutil.rmtree(RTD_DIR)
    RTD_DIR.mkdir(parents=True, exist_ok=True)

    # Statische Assets
    if (REPO_ROOT / "docs_assets").exists():
        for sub in ("javascripts", "stylesheets"):
            src = REPO_ROOT / "docs_assets" / sub
            if src.exists():
                shutil.copytree(src, RTD_DIR / sub, dirs_exist_ok=True)

    # Root-Dateien
    readme_txt = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_txt = (
        readme_txt.replace("(./PLAN.md)", "(PLAN.md)")
        .replace("(./VERBESSERUNGSPLAN.md)", "(VERBESSERUNGSPLAN.md)")
        .replace("(./comparison/reports/", "(comparison/reports/")
        .replace("(./comparison/)", "(comparison/reports/README.md)")
    )
    for b in VALID_BANKS:
        readme_txt = readme_txt.replace(f"(./{b}/ANALYSE_STRATEGIE.md)", f"({b}/ANALYSE_STRATEGIE.md)")
        readme_txt = readme_txt.replace(f"(./{b}/reports/", f"({b}/reports/")
        readme_txt = readme_txt.replace(f"(./{b}/)", f"({b}/reports/README.md)")
    readme_txt = _rewrite_github_links(readme_txt)
    (RTD_DIR / "index.md").write_text(readme_txt, encoding="utf-8")

    if (REPO_ROOT / "VERBESSERUNGSPLAN.md").exists():
        shutil.copy2(REPO_ROOT / "VERBESSERUNGSPLAN.md", RTD_DIR / "VERBESSERUNGSPLAN.md")

    plan_txt = (REPO_ROOT / "PLAN.md").read_text(encoding="utf-8")
    for b in VALID_BANKS:
        plan_txt = plan_txt.replace(f"./{b}/ANALYSE_STRATEGIE.md", f"banks/{b}/ANALYSE_STRATEGIE.md")
    plan_txt = _rewrite_github_links(plan_txt)
    (RTD_DIR / "PLAN.md").write_text(plan_txt, encoding="utf-8")

    # Comparison
    comp_dst = RTD_DIR / "comparison"
    comp_dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(REPO_ROOT / "comparison" / "reports", comp_dst / "reports", dirs_exist_ok=True)

    # Alle 19 Institute unter banks/
    for b in VALID_BANKS:
        cfg = load_bank_config(b)
        b_dst = RTD_DIR / "banks" / b
        b_dst.mkdir(parents=True, exist_ok=True)
        shutil.copytree(cfg.reports_dir, b_dst / "reports", dirs_exist_ok=True)
        if (cfg.bank_dir / "ANALYSE_STRATEGIE.md").exists():
            txt = _rewrite_github_links((cfg.bank_dir / "ANALYSE_STRATEGIE.md").read_text(encoding="utf-8"), b).replace("../PLAN.md", "../../PLAN.md")
            (b_dst / "ANALYSE_STRATEGIE.md").write_text(txt, encoding="utf-8")
        if (cfg.bank_dir / "ROADMAP.md").exists():
            txt = _rewrite_github_links((cfg.bank_dir / "ROADMAP.md").read_text(encoding="utf-8"), b).replace("../PLAN.md", "../../PLAN.md")
            (b_dst / "ROADMAP.md").write_text(txt, encoding="utf-8")
        if (cfg.data_dir / "validation_report.md").exists():
            shutil.copy2(cfg.data_dir / "validation_report.md", b_dst / "validation_report.md")

    print(f"[OK] .rtd_docs/ für Root, comparison/ und alle {len(VALID_BANKS)} Institute erzeugt.")
    return RTD_DIR


if __name__ == "__main__":
    prepare_docs()
