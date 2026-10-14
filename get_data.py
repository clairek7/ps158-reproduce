"""Download the Survey of Consumer Finances (SCF) summary extract files, 1989-2025.

Source: Board of Governors of the Federal Reserve System,
https://www.federalreserve.gov/econres/scfindex.htm

Each survey year has a "Summary Extract Public Data" file (the variables used
in the Fed's own report). The Fed publishes every year's extract with all dollar
variables already inflation-adjusted to 2025 dollars, so no further adjustment
is needed.

Also downloads the Fed's historical tables (2025 dollars), used to check our
numbers against the source's own published estimates.

Usage: python get_data.py
"""

import io
import urllib.request
import zipfile
from pathlib import Path

YEARS = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022, 2025]
BASE = "https://www.federalreserve.gov/econres/files/"
RAW = Path(__file__).parent / "data" / "raw"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ps158-reproduce (course assignment)"})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def main():
    RAW.mkdir(parents=True, exist_ok=True)

    for year in YEARS:
        out = RAW / f"scfp{year}.csv"
        if out.exists():
            print(f"{year}: already downloaded")
            continue
        url = f"{BASE}scfp{year}excel.zip"
        print(f"{year}: downloading {url}")
        with zipfile.ZipFile(io.BytesIO(fetch(url))) as z:
            csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if len(csvs) != 1:
                raise RuntimeError(f"expected one CSV in {url}, found {z.namelist()}")
            out.write_bytes(z.read(csvs[0]))

    tables = RAW / "scf2025_tables_public_real_historical.xlsx"
    if not tables.exists():
        print("downloading the Fed's historical tables (2025 dollars)")
        tables.write_bytes(fetch(BASE + tables.name))

    print(f"done: files in {RAW}")


if __name__ == "__main__":
    main()
