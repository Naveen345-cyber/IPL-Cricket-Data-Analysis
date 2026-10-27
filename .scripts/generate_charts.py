import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == '.scripts' else SCRIPT_DIR
os.chdir(PROJECT_ROOT)
os.makedirs('images', exist_ok=True)

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True

matches_path = 'data/ipl_matches.csv' if os.path.exists('data/ipl_matches.csv') else 'ipl_matches.csv'
players_path = 'data/ipl_player_stats.csv' if os.path.exists('data/ipl_player_stats.csv') else 'ipl_player_stats.csv'
matches = pd.read_csv(matches_path)
players = pd.read_csv(players_path)

print('MATCHES shape:', matches.shape)
print('PLAYERS shape:', players.shape)
print('Seasons:', sorted(matches['season'].unique().tolist()))

# ==================== 1. TEAM PERFORMANCE ====================
matches_played = pd.concat([matches['team1'], matches['team2']]).value_counts()
wins = matches['winner'].value_counts()
team_summary = pd.DataFrame({'matches_played': matches_played, 'wins': wins}).fillna(0)
team_summary['losses'] = team_summary['matches_played'] - team_summary['wins']
team_summary['win_pct'] = (team_summary['wins'] / team_summary['matches_played'] * 100).round(1)
team_summary = team_summary.sort_values('win_pct', ascending=False)

print('\n=== TEAM SUMMARY ===')
print(team_summary.to_string())

colors = ['#e74c3c','#f39c12','#2ecc71','#3498db','#9b59b6','#1abc9c','#e67e22','#e91e63','#00bcd4','#cddc39']
fig, ax = plt.subplots(figsize=(12,6))
bars = ax.bar(team_summary.index, team_summary['win_pct'], color=colors[:len(team_summary)])
ax.set_ylabel('Win Percentage (%)', fontsize=13)
ax.set_title('[Bar Chart] IPL Team Win Percentage (2020–2024)', fontsize=16, fontweight='bold')
ax.set_ylim(0, 80)
plt.xticks(rotation=40, ha='right', fontsize=11)
for bar, val in zip(bars, team_summary['win_pct']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val}%', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('images/chart_1_team_win_pct.png', dpi=150)
plt.close()
print('Saved chart_1_team_win_pct.png')

top3_teams = team_summary.head(3).index.tolist()
season_wins = matches[matches['winner'].isin(top3_teams)].groupby(['season','winner']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12,6))
for team in top3_teams:
    if team in season_wins.columns:
        ax.plot(season_wins.index, season_wins[team], marker='o', linewidth=2.5, markersize=8, label=team)
ax.set_xlabel('Season', fontsize=13)
ax.set_ylabel('Wins', fontsize=13)
ax.set_title('[Line Chart] Season-wise Wins Trend (Top 3 Teams)', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig('images/chart_2_season_wins_trend.png', dpi=150)
plt.close()
print('Saved chart_2_season_wins_trend.png')

# ==================== 2. PLAYER STATISTICS ====================
batting_summary = players.groupby('player').agg(
    total_runs=('runs_scored','sum'),
    innings=('match_id','count'),
    balls_faced=('balls_faced','sum'),
    fours=('fours','sum'),
    sixes=('sixes','sum')
)
batting_summary['strike_rate'] = np.where(
    batting_summary['balls_faced'] > 0,
    (batting_summary['total_runs'] / batting_summary['balls_faced']) * 100, 0
).round(1)
batting_summary['avg_runs'] = (batting_summary['total_runs'] / batting_summary['innings']).round(1)

bowling_summary = players.groupby('player').agg(
    total_wickets=('wickets_taken','sum'),
    overs_bowled=('overs_bowled','sum'),
    runs_conceded=('runs_conceded','sum')
)
bowling_summary['economy'] = np.where(
    bowling_summary['overs_bowled'] > 0,
    bowling_summary['runs_conceded'] / bowling_summary['overs_bowled'], 0
).round(2)

top_run_scorers = batting_summary.sort_values('total_runs', ascending=False).head(10)
top_wicket_takers = bowling_summary[bowling_summary['total_wickets'] > 0].sort_values('total_wickets', ascending=False).head(10)

print('\n=== TOP 10 RUN SCORERS ===')
print(top_run_scorers[['total_runs','strike_rate','fours','sixes']].to_string())
print('\n=== TOP 10 WICKET TAKERS ===')
print(top_wicket_takers[['total_wickets','economy']].to_string())

fig, ax = plt.subplots(figsize=(12,7))
bars = ax.barh(top_run_scorers.index[::-1], top_run_scorers['total_runs'][::-1], color='#f39c12')
ax.set_xlabel('Total Runs', fontsize=13)
ax.set_title('[Horizontal Bar Chart] Top 10 IPL Run Scorers', fontsize=16, fontweight='bold')
for bar, val in zip(bars, top_run_scorers['total_runs'][::-1]):
    ax.text(bar.get_width()+5, bar.get_y()+bar.get_height()/2, str(int(val)), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/chart_3_top_run_scorers.png', dpi=150)
plt.close()
print('Saved chart_3_top_run_scorers.png')

fig, ax = plt.subplots(figsize=(12,7))
bars = ax.barh(top_wicket_takers.index[::-1], top_wicket_takers['total_wickets'][::-1], color='#2ecc71')
ax.set_xlabel('Total Wickets', fontsize=13)
ax.set_title('[Horizontal Bar Chart] Top 10 IPL Wicket Takers', fontsize=16, fontweight='bold')
for bar, val in zip(bars, top_wicket_takers['total_wickets'][::-1]):
    ax.text(bar.get_width()+0.2, bar.get_y()+bar.get_height()/2, str(int(val)), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/chart_4_top_wicket_takers.png', dpi=150)
plt.close()
print('Saved chart_4_top_wicket_takers.png')

# ==================== 3. TOSS ANALYSIS ====================
matches['toss_match_same'] = matches['toss_winner'] == matches['winner']
toss_win_rate = matches['toss_match_same'].mean() * 100
contingency = pd.crosstab(matches['toss_decision'], matches['toss_match_same'])
chi2, p_value, dof, expected = chi2_contingency(contingency)
decision_outcome = matches.groupby('toss_decision')['toss_match_same'].mean() * 100

print(f'\nToss win rate: {toss_win_rate:.1f}%')
print(f'Chi2={chi2:.2f}, p={p_value:.4f}')
print('Decision outcome:', decision_outcome.round(1).to_dict())

fig, ax = plt.subplots(figsize=(8,6))
bars = ax.bar(decision_outcome.index, decision_outcome.values, color=['#e74c3c','#9b59b6'], width=0.5)
ax.set_ylabel('Win Rate (%)', fontsize=13)
ax.set_title('[Bar Chart] Bat vs Field — Toss Decision Win Rate', fontsize=16, fontweight='bold')
ax.set_ylim(0, 80)
for bar, val in zip(bars, decision_outcome.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('images/chart_5_toss_decision_winrate.png', dpi=150)
plt.close()
print('Saved chart_5_toss_decision_winrate.png')

runs_margins = matches.loc[matches['win_by_runs'] > 0, 'win_by_runs']
wickets_margins = matches.loc[matches['win_by_wickets'] > 0, 'win_by_wickets']
fig, ax = plt.subplots(figsize=(10,6))
ax.hist(runs_margins, bins=15, color='#17becf', edgecolor='black', alpha=0.85)
ax.set_xlabel('Win Margin (Runs)', fontsize=13)
ax.set_ylabel('Number of Matches', fontsize=13)
ax.set_title('[Histogram] Distribution of Winning Margins (Runs)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('images/chart_6_win_margin_runs.png', dpi=150)
plt.close()
print('Saved chart_6_win_margin_runs.png')

# ==================== 4. VENUE ANALYSIS ====================
venue_scores = matches.groupby('venue')['team1_score'].mean().sort_values(ascending=False).round(1)
print('\n=== VENUE SCORES ===')
print(venue_scores.to_string())

fig, ax = plt.subplots(figsize=(13,8))
bars = ax.barh(venue_scores.index[::-1], venue_scores.values[::-1], color='#3498db')
ax.set_xlabel('Avg 1st Innings Score', fontsize=13)
ax.set_title('[Horizontal Bar Chart] Average 1st Innings Score by Venue', fontsize=16, fontweight='bold')
for bar, val in zip(bars, venue_scores.values[::-1]):
    ax.text(bar.get_width()+0.5, bar.get_y()+bar.get_height()/2, str(val), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/chart_7_venue_scores.png', dpi=150)
plt.close()
print('Saved chart_7_venue_scores.png')

# ==================== 5. PLAYER OF THE MATCH ====================
potm = matches['player_of_match'].value_counts().head(10)
print('\n=== POTM ===')
print(potm.to_string())

fig, ax = plt.subplots(figsize=(12,7))
bars = ax.barh(potm.index[::-1], potm.values[::-1], color='#e91e63')
ax.set_xlabel('Player of the Match Awards', fontsize=13)
ax.set_title('[Horizontal Bar Chart] Top 10 Player of the Match Winners', fontsize=16, fontweight='bold')
for bar, val in zip(bars, potm.values[::-1]):
    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2, str(int(val)), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/chart_8_potm.png', dpi=150)
plt.close()
print('Saved chart_8_potm.png')

# ==================== 6. SIXES & FOURS by SEASON ====================
season_bnd = players.groupby('season').agg(total_fours=('fours','sum'), total_sixes=('sixes','sum'))

fig, ax = plt.subplots(figsize=(12,6))
width = 0.4
x = np.arange(len(season_bnd))
ax.bar(x - width/2, season_bnd['total_fours'], width=width, label='Fours', color='#3498db', alpha=0.85)
ax.bar(x + width/2, season_bnd['total_sixes'], width=width, label='Sixes', color='#e74c3c', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(season_bnd.index.astype(str), rotation=30)
ax.set_xlabel('Season', fontsize=13)
ax.set_ylabel('Count', fontsize=13)
ax.set_title('[Grouped Bar Chart] Boundary Trends: Fours vs Sixes Per Season', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig('images/chart_9_season_boundaries.png', dpi=150)
plt.close()
print('Saved chart_9_season_boundaries.png')

# ==================== KEY STATS ====================
total_matches = len(matches)
total_seasons = matches['season'].nunique()
total_teams = matches['team1'].nunique()
total_players = players['player'].nunique()
avg_score = matches['team1_score'].mean()
champion_team = team_summary.head(1).index[0]
champion_winpct = team_summary['win_pct'].max()
top_scorer_name = top_run_scorers.index[0]
top_scorer_runs = int(top_run_scorers['total_runs'].iloc[0])
top_wkt_name = top_wicket_takers.index[0]
top_wkt_count = int(top_wicket_takers['total_wickets'].iloc[0])

print('\n=== KEY STATS ===')
print('total_matches:', total_matches)
print('total_seasons:', total_seasons)
print('total_teams:', total_teams)
print('total_players:', total_players)
print('avg_score:', round(avg_score, 1))
print('toss_win_rate:', round(toss_win_rate, 1))
print('champion_team:', champion_team)
print('champion_winpct:', champion_winpct)
print('top_scorer_name:', top_scorer_name)
print('top_scorer_runs:', top_scorer_runs)
print('top_wkt_name:', top_wkt_name)
print('top_wkt_count:', top_wkt_count)
print('p_value:', round(p_value, 4))
print('chi2:', round(chi2, 2))
print('runs_margins_mean:', round(runs_margins.mean(), 1))
print('wickets_margins_mean:', round(wickets_margins.mean(), 1))
print('total_fours:', int(batting_summary['fours'].sum()))
print('total_sixes:', int(batting_summary['sixes'].sum()))

print('\nAll done!')
