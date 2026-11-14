"""Step 7: summary table and figure for the dashboard.

Writes to outputs/ (or outputs/sample/ with --sample):
  summary_by_trade_type.csv : trade_type, n, mean_car, std_car, t_stat, t_used
  car_by_trade_type.png     : mean CAR by trade type with 95% confidence intervals
Filters (size, 10b5-1) come from src/config.py. Events overlapping in time are not
independent, so t-stats are descriptive; see README Threats.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analyst_io as aio  # noqa: E402


def summarize(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = [(k, g) for k, g in events.groupby("trade_type")] + [("all", events)]
    for name, g in groups:
        n = len(g)
        mean = g["CAR"].mean()
        std = g["CAR"].std(ddof=1) if n > 1 else np.nan
        t_stat = mean / (std / np.sqrt(n)) if n > 1 and std > 0 else np.nan
        rows.append(dict(trade_type=name, n=n, mean_car=mean, std_car=std,
                         t_stat=t_stat, t_used=int(g["t_used"].max())))
    return pd.DataFrame(rows)


def plot(summary: pd.DataFrame, path) -> None:
    s = summary[summary["trade_type"] != "all"]
    se = s["std_car"] / np.sqrt(s["n"])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(s["trade_type"], s["mean_car"], yerr=1.96 * se, capsize=4)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel(f"Mean CAR through t = {int(s['t_used'].max())}")
    ax.set_title("Abnormal return after the filing date, by trade type")
    for i, n in enumerate(s["n"]):
        ax.text(i, 0.02, f"n={n}", ha="center", va="bottom", fontsize=9,
                transform=ax.get_xaxis_transform())
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    args = aio.parse_args(__doc__)
    tx_path, panel_path, out_dir = aio.paths(args.sample)
    aio.require(tx_path, "transactions.csv")
    aio.require(panel_path, "event_panel.csv")
    events = aio.event_car(aio.load_transactions(tx_path), aio.load_panel(panel_path))
    if events.empty:
        raise SystemExit("No events left after filters; nothing to report.")
    summary = summarize(events)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_dir / "summary_by_trade_type.csv", index=False)
    plot(summary, out_dir / "car_by_trade_type.png")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
