"""Plot mean family net worth by parents' education, 1989-2025, from the SCF.

Reads the summary extract files downloaded by get_data.py, computes weighted
mean net worth for families with children by the education of the SCF
reference person, saves the numbers to data/wealth_by_parent_education.csv,
and draws figure.png as a black-and-white academic journal figure.

Definitions:
  - Families with children: at least one child of the reference person
    living at home (KIDS > 0).
  - BA or more: EDCL == 4 (college degree). HS or less: EDCL in {1, 2}.
  - Net worth: NETWORTH, already in 2025 dollars in the Fed's extract files.
  - Each family appears five times (one row per implicate); WGT is already
    divided across the five, so a weighted mean over all rows is correct.

Usage: python plot.py   (run get_data.py first)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from get_data import RAW, YEARS

HERE = Path(__file__).parent
GROUPS = {"BA or more": [4], "HS or less": [1, 2]}


def load_year(year):
    df = pd.read_csv(RAW / f"scfp{year}.csv")
    df.columns = df.columns.str.upper()
    return df[["WGT", "EDCL", "KIDS", "NETWORTH"]]


def summarize():
    rows = []
    for year in YEARS:
        df = load_year(year)
        df = df[df["KIDS"] > 0]
        for group, codes in GROUPS.items():
            g = df[df["EDCL"].isin(codes)]
            rows.append({
                "year": year,
                "group": group,
                "mean_networth": (g["WGT"] * g["NETWORTH"]).sum() / g["WGT"].sum(),
                "n_families": len(g) // 5,
            })
    return pd.DataFrame(rows)


def plot(summary):
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(6.5, 5.2))

    styles = {
        "BA or more": dict(linestyle="-", marker="o", markerfacecolor="white"),
        "HS or less": dict(linestyle="--", marker="s", markerfacecolor="white"),
    }
    for group, style in styles.items():
        d = summary[summary["group"] == group]
        ax.plot(d["year"], d["mean_networth"] / 1000, color="black", linewidth=1.2,
                markersize=5, label=group, **style)

    ax.set_xlabel("Survey year")
    ax.set_ylabel("Mean net worth (thousands of 2025 dollars)")
    ax.set_xticks(YEARS)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.legend(title="Reference person's education", frameon=False, loc="upper left")

    caption = (
        "Figure 1. Mean net worth of families with children, by parents' education, 1989–2025.\n"
        "Notes: Families with at least one child of the reference person living at home. Education\n"
        "of the SCF reference person. Weighted with SCF sample weights across all five implicates.\n"
        "Dollar values as published by the Federal Reserve, inflation-adjusted to 2025 dollars.\n"
        "Source: Board of Governors of the Federal Reserve System, Survey of Consumer Finances,\n"
        "summary extract public data."
    )
    fig.text(0.02, 0.01, caption, ha="left", va="bottom", fontsize=8.5, linespacing=1.4)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.33)
    fig.savefig(HERE / "figure.png", dpi=200)


def main():
    summary = summarize()
    out = HERE / "data" / "wealth_by_parent_education.csv"
    summary.to_csv(out, index=False, float_format="%.0f")
    print(summary.pivot(index="year", columns="group", values="mean_networth").round(-3).to_string())
    plot(summary)
    print(f"saved {out.name} and figure.png")


if __name__ == "__main__":
    main()
