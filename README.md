# WBBL Cricket Win Score – open data

Open data and dashboard for: Mondal, S. (2026). *A win-based measure of player productivity in cricket: evidence from the Women's Big Bash League between 2016/17 and 2025/26.* Managing Sport and Leisure. https://doi.org/10.1080/23750472.2026.2747309

- `data/` – tidy CSVs: player-season (batting, bowling, combined), team-season, model coefficients.
- `dashboard/index.html` – self-contained dashboard (open locally or host on GitHub Pages).
- `scripts/` – `build_data.py` (workbooks → CSV, prints the paper's MAE and correlation) and `build_dashboard.py`.
- `docs/DATA_DICTIONARY.md` – every column and unit.

Rebuild: `python scripts/build_data.py batter.xlsx bowler.xlsx data && python scripts/build_dashboard.py` (requires pandas, openpyxl).

Licences: data CC BY 4.0, code MIT (the paper itself is CC BY-NC-ND). Cite via `CITATION.cff`.
