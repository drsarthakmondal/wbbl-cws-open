"""Embed the CSVs into dashboard/template.html -> dashboard/index.html (self-contained, works from file:// or GitHub Pages)."""
import json, pandas as pd, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
rd = lambda n: pd.read_csv(root/"data"/f"{n}.csv").round(6).where(lambda d: d.notna(), "").to_dict("records")
data = {"players": rd("player_season_all"), "teams": rd("team_season"), "coef": rd("model_coefficients")}
html = (root/"dashboard"/"template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(root/"dashboard"/"index.html").write_text(html); print(len(html)//1024, "KB")
