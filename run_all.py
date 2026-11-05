"""Run the pipeline. Each step is skipped if its outputs already exist.

    python run_all.py            # run missing steps
    python run_all.py --force    # rebuild every step
    python run_all.py --sample   # only validate data/sample/ against the contracts

Lane owners add their script to STEPS (one line). Steps whose script does not
exist yet are reported as "not implemented" and do not fail the run.
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import config  # noqa: E402
import contracts  # noqa: E402

# (step name, script, outputs, owner)
STEPS = [
    ("fetch_sec", "src/fetch_sec.py", [config.DATA_RAW / "sec_done.flag"], "A"),
    ("build_transactions", "src/build_transactions.py", [config.TRANSACTIONS_CSV], "A"),
    ("sp500_membership", "src/sp500_membership.py", [config.DATA_OUTPUT / "sp500_membership.csv"], "A"),
    ("fetch_prices", "src/fetch_prices.py", [config.DATA_RAW / "prices_done.flag"], "B"),
    ("event_study", "src/event_study.py", [config.EVENT_PANEL_CSV], "B"),
    ("classify_insiders", "src/classify_insiders.py", [config.DATA_OUTPUT / "classified.flag"], "C"),
    ("report", "src/report.py", [config.OUTPUTS / "summary.csv"], "C"),
]


def run_step(name: str, script: str, outputs: list[Path], force: bool) -> str:
    """Skip-if-exists helper. Returns 'skipped', 'ran', 'not implemented' or 'FAILED'."""
    path = config.ROOT / script
    if not path.exists():
        return "not implemented"
    if not force and all(p.exists() for p in outputs):
        return "skipped"
    result = subprocess.run([sys.executable, str(path)], cwd=config.ROOT)
    return "ran" if result.returncode == 0 else "FAILED"


def check_sample() -> list[str]:
    return (contracts.validate_transactions(config.SAMPLE_TRANSACTIONS_CSV)
            + contracts.validate_event_panel(config.SAMPLE_EVENT_PANEL_CSV))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="rerun steps even if outputs exist")
    ap.add_argument("--sample", action="store_true", help="validate data/sample/ only")
    args = ap.parse_args()

    if args.sample:
        problems = check_sample()
        print("sample contracts:", "OK" if not problems else "\n  ".join(["PROBLEMS"] + problems))
        return 1 if problems else 0

    failed = False
    for name, script, outputs, owner in STEPS:
        status = run_step(name, script, outputs, args.force)
        print(f"[{owner}] {name:<20} {status}")
        failed |= status == "FAILED"
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
