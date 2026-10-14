# ps158-reproduce

Wealth by parents' education, 1989–2025
POLISCI 158, Section Assignment 3, Option B: reproducing the Section 3 demo figure.

Figure 1

Figure 1 shows the mean net worth of US families with children, by the parents' education (BA or more vs. high school or less), for every Survey of Consumer Finances from 1989 to 2025, in 2025 dollars. In 2025, families whose parents have a BA or more had about $2.29 million on average, and families whose parents have a high-school education or less had about $269,000.

Data
Federal Reserve Board, Survey of Consumer Finances (SCF), summary extract public data, 1989–2025 (earlier years are listed under previous surveys). get_data.py downloads the CSV extract for each year (scfp{year}excel.zip) and the Fed's historical tables in 2025 dollars.

Choices behind the numbers:

Families: families with at least one child of the reference person living at home (KIDS > 0).
Education: that of the SCF reference person. "BA or more" is EDCL == 4; "HS or less" is EDCL 1 or 2.
Dollars: the Fed publishes every year's extract already adjusted to 2025 dollars, so the code doesn't adjust them again.
Weights: each family appears five times (one per implicate); estimates use the survey weight WGT across all rows.
How to rerun
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python get_data.py   # downloads about 340 MB into data/raw/
.venv/bin/python plot.py       # writes figure.png and data/wealth_by_parent_education.csv
Files
get_data.py: downloads the data from the Federal Reserve
plot.py: computes weighted means and draws the figure
figure.png: the reproduced figure
data/wealth_by_parent_education.csv: the numbers plotted in the figure
