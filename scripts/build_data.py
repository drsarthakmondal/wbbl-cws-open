"""Build the tidy open CWS dataset from the two author workbooks.
Usage: python build_data.py <batter.xlsx> <bowler.xlsx> <out_dir>
Reads cached cell values (the workbooks are the calculation record)."""
import sys, re, pandas as pd, numpy as np
bat_x, bowl_x, out = sys.argv[1:4]
SEASONS = [f"{y}-{str(y+1)[2:]}" for y in range(2016, 2026)]
# matches per team per season = points denominator / 2 (from Calculations sheets: 28 pts -> 14 matches; 20 -> 10)
def sheet_season(s): return s.replace("-", "/")

def load(path, kind):
    x = pd.ExcelFile(path); frames = []
    for s in SEASONS:
        d = x.parse(s).rename(columns=lambda c: c.strip())
        d = d.rename(columns={"balls_per_innings": "ball_per_innings"})
        d["season"] = sheet_season(s)
        if kind == "bat":
            d = d.rename(columns={"BATPROD": "bat_prod", "TADJ": "bat_prod_team_adj",
                "median_batting_position": "batting_role", "number_of_innings_batted": "innings_batted",
                "runs_off_bat": "runs_scored", "WINPCT": "cws_general", "WINPADJ": "cws_role_adj"})
            keep = ["season","player_name","team_name","batting_role","innings_batted","runs_scored",
                    "balls_faced","wickets_lost","bat_prod","bat_prod_team_adj","cws_general","cws_role_adj"]
        else:
            d = d.rename(columns={"BOWLPROD": "bowl_prod", "BALLPROD": "bowl_prod", "TADJ": "bowl_prod_team_adj",
                "number_of_innings_bowled": "innings_bowled", "ball_per_innings": "bowling_role",
                "WINPCT": "cws_general", "WINPADJ": "cws_role_adj"})
            keep = ["season","player_name","team_name","bowling_role","innings_bowled","runs_conceded",
                    "balls_bowled","wickets_taken","bowl_prod","bowl_prod_team_adj","cws_general","cws_role_adj"]
        frames.append(d[keep])
    return pd.concat(frames, ignore_index=True)

bat = load(bat_x, "bat"); bowl = load(bowl_x, "bowl")
bat.insert(0, "discipline", "batting"); bowl.insert(0, "discipline", "bowling")

# team-season table
tb = pd.read_excel(bat_x, "Calculations_Correct")
tb = tb[tb.team.ne("Total") & tb.team.notna()].iloc[:80]
tb = tb[["season","team","Pts","WINPCT","balls_faced","wickets_lost","runs_scored_off_extras"]].rename(columns={
    "Pts":"points","WINPCT":"win_pct","runs_scored_off_extras":"runs_off_extras_batting"})
tw = pd.read_excel(bowl_x, "Calculations_Actual")
tw = tw[tw.team.ne("Total") & tw.team.notna()].iloc[:80]
tw = tw[["season","team","balls_bowled","wickets_taken","wickets_taken_run_out_obstructing_the_field",
         "runs_conceded_off_byes_legbyes_penalties"]].rename(columns={
    "wickets_taken_run_out_obstructing_the_field":"wickets_not_credited_to_bowlers",
    "runs_conceded_off_byes_legbyes_penalties":"runs_conceded_extras_unattributed"})
team = tb.merge(tw, on=["season","team"], validate="1:1")
team["matches"] = np.where(team.season.isin(["2024/25","2025/26"]), 10, 14)   # 28-point seasons = 14 matches; 20-point seasons (2024/25, 2025/26) = 10
team["wins_equiv"] = team.win_pct * team.matches

# aggregate CWS to team-season (validation, Berri-style)
agg = (pd.concat([bat, bowl]).groupby(["season","team_name"])[["cws_general","cws_role_adj"]].sum()
       .rename(columns=lambda c: "sum_"+c).reset_index().rename(columns={"team_name":"team"}))
team = team.merge(agg, on=["season","team"], how="left", validate="1:1")
team["abs_error_general"] = (team.sum_cws_general - team.win_pct).abs()
team["abs_error_role_adj"] = (team.sum_cws_role_adj - team.win_pct).abs()
bat.to_csv(f"{out}/batter_player_season.csv", index=False)
bowl.to_csv(f"{out}/bowler_player_season.csv", index=False)
team.to_csv(f"{out}/team_season.csv", index=False)
print(len(bat), len(bowl), len(team))
print("MAE general", team.abs_error_general.mean(), "MAE role", team.abs_error_role_adj.mean())
print("corr", np.corrcoef(team.sum_cws_general, team.win_pct)[0,1], np.corrcoef(team.sum_cws_role_adj, team.win_pct)[0,1])
print(team.groupby("season").abs_error_general.mean().round(3).to_dict())
