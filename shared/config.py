"""Deklarativer Konfigurations-Loader und Schema-Validator für <bank>/bank_config.yaml."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BANKS_DIR = REPO_ROOT / "banks"

VALID_BANKS = (
    "bekb",
    "vskb",
    "zkb",
    "bcv",
    "gekb",
    "raiffeisen",
    "postfinance",
    "ubs",
    "eks",
    "slm",
    "aek",
    "migrosbank",
    "vontobel",
    "pictet",
    "entris",
    "valiant",
    "sgkb",
    "lukb",
    "blkb",
    "fkb",
)
VALID_SCOPES = {"standalone", "consolidated"}
VALID_REPORT_05_MODES = {"listed_share", "cantonal_endowment", "cooperative_payout", "post_dividend"}
VALID_PEER_GROUPS = {
    "cantonal_bank",
    "domestic_dsib",
    "g_sib",
    "regional_bank",
    "wealth_manager",
    "private_bank",
}


@dataclass
class BankConfig:
    bank_id: str
    short_name: str
    full_name: str
    peer_group: str
    canton_or_hq: str
    legal_form: str
    listed: bool
    ticker: str | None
    state_guarantee: bool
    has_credit_ban: bool
    finma_category: int
    reporting_scope: str
    accounting_standard: str
    reporting_currency: str
    primary_languages: list[str]
    file_prefix: str
    capital_targets_pct: dict[str, float]
    share_splits: list[dict[str, Any]]
    report_05_mode: str
    report_05_slug: str
    palette: dict[str, str]
    plausibility_bounds_chf_mio: dict[str, float]
    epochs: list[dict[str, Any]]
    structural_breaks: list[dict[str, Any]] = field(default_factory=list)
    chunk_anchors: dict[str, list[str]] = field(default_factory=dict)
    public_share_pct_default: float | None = None
    default_unit: str | None = None
    notes: str = ""

    @property
    def bank_dir(self) -> Path:
        return BANKS_DIR / self.bank_id

    @property
    def md_dir(self) -> Path:
        return self.bank_dir / ".md"

    @property
    def data_dir(self) -> Path:
        return self.bank_dir / "data"

    @property
    def chunks_dir(self) -> Path:
        return self.data_dir / "chunks"

    @property
    def extracted_dir(self) -> Path:
        return self.data_dir / "extracted"

    @property
    def reports_dir(self) -> Path:
        return self.bank_dir / "reports"

    @property
    def charts_dir(self) -> Path:
        return self.reports_dir / "charts"


REQUIRED_FIELDS = [
    "bank_id",
    "short_name",
    "full_name",
    "peer_group",
    "canton_or_hq",
    "legal_form",
    "listed",
    "state_guarantee",
    "finma_category",
    "reporting_scope",
    "accounting_standard",
    "reporting_currency",
    "primary_languages",
    "file_prefix",
    "capital_targets_pct",
    "report_05_mode",
    "report_05_slug",
    "palette",
    "epochs",
]


def load_bank_config(bank_id: str, root: Path | None = None) -> BankConfig:
    base = root or BANKS_DIR
    cfg_path = base / bank_id / "bank_config.yaml"
    if not cfg_path.exists():
        raise FileNotFoundError(f"Konfiguration nicht gefunden: {cfg_path}")

    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    missing = [k for k in REQUIRED_FIELDS if k not in raw]
    if missing:
        raise ValueError(f"{cfg_path}: Fehlende Pflichtfelder: {missing}")

    if raw["reporting_scope"] not in VALID_SCOPES:
        raise ValueError(f"{cfg_path}: Ungültiger reporting_scope '{raw['reporting_scope']}'")
    if raw["report_05_mode"] not in VALID_REPORT_05_MODES:
        raise ValueError(f"{cfg_path}: Ungültiger report_05_mode '{raw['report_05_mode']}'")
    if raw["peer_group"] not in VALID_PEER_GROUPS:
        raise ValueError(f"{cfg_path}: Ungültiger peer_group '{raw['peer_group']}'")
    if int(raw["finma_category"]) not in (1, 2, 3, 4, 5):
        raise ValueError(f"{cfg_path}: Ungültige finma_category '{raw['finma_category']}'")

    return BankConfig(
        bank_id=str(raw["bank_id"]),
        short_name=str(raw["short_name"]),
        full_name=str(raw["full_name"]),
        peer_group=str(raw["peer_group"]),
        canton_or_hq=str(raw["canton_or_hq"]),
        legal_form=str(raw["legal_form"]),
        listed=bool(raw["listed"]),
        ticker=raw.get("ticker"),
        state_guarantee=bool(raw["state_guarantee"]),
        has_credit_ban=bool(raw.get("has_credit_ban", False)),
        finma_category=int(raw["finma_category"]),
        reporting_scope=str(raw["reporting_scope"]),
        accounting_standard=str(raw["accounting_standard"]),
        reporting_currency=str(raw["reporting_currency"]),
        primary_languages=list(raw["primary_languages"]),
        file_prefix=str(raw["file_prefix"]),
        capital_targets_pct={k: float(v) for k, v in raw["capital_targets_pct"].items()},
        share_splits=list(raw.get("share_splits", [])),
        report_05_mode=str(raw["report_05_mode"]),
        report_05_slug=str(raw["report_05_slug"]),
        palette={k: str(v) for k, v in raw["palette"].items()},
        plausibility_bounds_chf_mio={k: float(v) for k, v in raw.get("plausibility_bounds_chf_mio", {}).items()},
        epochs=list(raw["epochs"]),
        structural_breaks=list(raw.get("structural_breaks", [])),
        chunk_anchors=dict(raw.get("chunk_anchors", {})),
        public_share_pct_default=raw.get("public_share_pct_default"),
        default_unit=raw.get("default_unit"),
        notes=str(raw.get("notes", "")),
    )


def check_all_schemas(root: Path | None = None) -> list[str]:
    base = root or BANKS_DIR
    checked = []
    for b in VALID_BANKS:
        cfg_path = base / b / "bank_config.yaml"
        if cfg_path.exists():
            load_bank_config(b, root=base)
            checked.append(b)
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description="Validiert <bank>/bank_config.yaml Schemas.")
    parser.add_argument("--check-schema", action="store_true", help="Prüft alle vorhandenen bank_config.yaml Dateien.")
    parser.add_argument("--bank", help="Prüft eine spezifische Bank-Konfiguration.")
    args = parser.parse_args()

    if args.bank:
        cfg = load_bank_config(args.bank)
        print(f"[OK] {cfg.bank_id}: {cfg.full_name} ({cfg.reporting_scope}, {cfg.reporting_currency})")
    elif args.check_schema:
        checked = check_all_schemas()
        print(f"[OK] Schema-Check bestanden für: {', '.join(checked) if checked else 'keine bank_config.yaml bisher vorhanden'}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
