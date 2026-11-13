# Data dictionary

All values are produced by the author's workbooks (`WBBL_batter_stats.xlsx`, `WBBL_bowler_stats.xlsx`) and harmonised by `scripts/build_data.py`. Season labels use `2016/17` style.

**Units.** CWS is in team win-percentage points (1.0 = 100 percentage points of a team's winning percentage). Per season the league sums to 2.0 for all batters and 2.0 for all bowlers; a team's batters plus bowlers sum to approximately its winning percentage. Multiply by team matches for win-equivalents (`team_season.wins_equiv`).

## player_season_all.csv (1,746 rows; also split by discipline)
| Column | Meaning |
|---|---|
| discipline | `batting` or `bowling`. A player who bats and bowls has a row in each. |
| season, player_name, team_name | Key is season + player + team (RA Mair 2020/21 appears for two teams). |
| role | Batting: median batting position band (Top Order 1–3, Upper Middle 4–6, Lower Middle 7–8, Lower Order 9–11). Bowling: Type 1 (1–12 balls/match), Type 2 (13–18), Type 3 (19–24). |
| innings | Innings batted / bowled. |
| runs | Runs off the bat (batting) or runs conceded (bowling). |
| balls | Legal balls faced / bowled. |
| wickets | Wickets lost (batting) or wickets taken (bowling). |
| prod | BATPROD / BOWLPROD: 0.0012·runs − 0.0014·balls − 0.0031·wkts lost (batting); 0.0014·balls − 0.0012·runs + 0.0031·wkts (bowling). |
| prod_team_adj | `prod` after removing team effects (TADJ in the workbooks). |
| cws_general | CWS against the league-wide average batter/bowler (workbook `WINPCT`). |
| cws_role_adj | CWS against the role benchmark (workbook `WINPADJ`). |

## team_season.csv (80 rows)
season, team, points, win_pct (= points / (2 × matches)), team balls faced/bowled, wickets lost/taken, unattributed extras and wickets, matches (14 for 2016/17–2023/24, 10 for 2024/25–2025/26), wins_equiv, sum_cws_general, sum_cws_role_adj (summed over the team's batters and bowlers), abs_error_* (|summed CWS − win_pct|).
Reproduces the paper: MAE 0.106, correlation 0.852 (general specification).

## model_coefficients.csv
Coefficients transcribed from Tables 1–5 of the paper.

## Known caveats
- The workbooks use slightly different intermediate columns across seasons (e.g. `TADJ1`, `ADJPROD1`, `WINBALL1` in 2016/17 and 2025/26). Only the columns common to all seasons are published; the final CWS columns are consistent.
- The paper's inclusion thresholds for reporting are 50 balls faced (batters) and 30 balls bowled (bowlers); the data contain all players.
- Source ball-by-ball data: Cricsheet (check its licence before redistributing raw deliveries).
