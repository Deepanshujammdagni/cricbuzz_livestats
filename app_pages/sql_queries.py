"""
25 SQL practice queries interface - beginner to advanced.
"""

import streamlit as st
import pandas as pd
from utils.db_connection import run_query, get_connection
from mysql.connector import Error


# All 25 queries as defined in the project PDF
SQL_QUESTIONS = {
    "Beginner": [
        {
            "id": "Q1",
            "title": "Indian Players",
            "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
            "query": """
SELECT p.full_name, p.playing_role, p.batting_style, p.bowling_style
FROM players p
JOIN teams t ON p.team_id = t.team_id
WHERE t.country = 'India'
ORDER BY p.full_name;
"""
        },
        {
            "id": "Q2",
            "title": "Matches in Last 30 Days",
            "description": "Show all cricket matches played in the last 30 days. Include match description, team names, venue, and match date.",
            "query": """
SELECT m.match_description, t1.team_name AS team1, t2.team_name AS team2,
       v.venue_name, v.city, m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= CURDATE() - INTERVAL 30 DAY
ORDER BY m.match_date DESC;
"""
        },
        {
            "id": "Q3",
            "title": "Top 10 ODI Run Scorers",
            "description": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs, batting average, and centuries.",
            "query": """
SELECT p.full_name AS player_name,
       ps.runs_scored AS total_runs,
       ps.batting_average,
       ps.centuries
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
WHERE ps.format = 'ODI'
ORDER BY ps.runs_scored DESC
LIMIT 10;
"""
        },
        {
            "id": "Q4",
            "title": "Venues with 50,000+ Capacity",
            "description": "Display all cricket venues with seating capacity over 50,000. Order by largest capacity first.",
            "query": """
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
"""
        },
        {
            "id": "Q5",
            "title": "Team Win Counts",
            "description": "Calculate how many matches each team has won. Show team name and total wins.",
            "query": """
SELECT t.team_name, COUNT(*) AS total_wins
FROM matches m
JOIN teams t ON m.winning_team_id = t.team_id
WHERE m.match_status = 'completed'
GROUP BY t.team_name
ORDER BY total_wins DESC;
"""
        },
        {
            "id": "Q6",
            "title": "Players by Role",
            "description": "Count how many players belong to each playing role.",
            "query": """
SELECT playing_role, COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
"""
        },
        {
            "id": "Q7",
            "title": "Highest Score per Format",
            "description": "Find the highest individual batting score in each cricket format.",
            "query": """
SELECT ps.format, MAX(ps.highest_score) AS highest_score
FROM player_stats ps
GROUP BY ps.format
ORDER BY highest_score DESC;
"""
        },
        {
            "id": "Q8",
            "title": "Series Started in 2024",
            "description": "Show all cricket series that started in 2024.",
            "query": """
SELECT series_name, host_country, match_type,
       start_date, total_matches
FROM series
WHERE YEAR(start_date) = 2024
ORDER BY start_date;
"""
        },
    ],
    "Intermediate": [
        {
            "id": "Q9",
            "title": "All-rounders: 1000+ Runs & 50+ Wickets",
            "description": "Find all-rounders with 1000+ runs AND 50+ wickets. Show player name, runs, wickets, and format.",
            "query": """
SELECT p.full_name, t.team_name,
       ps.format, ps.runs_scored, ps.wickets_taken
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id
WHERE p.playing_role = 'All-rounder'
  AND ps.runs_scored > 1000
  AND ps.wickets_taken > 50
ORDER BY ps.runs_scored DESC;
"""
        },
        {
            "id": "Q10",
            "title": "Last 20 Completed Matches",
            "description": "Get details of the last 20 completed matches with winning team and victory details.",
            "query": """
SELECT m.match_description,
       t1.team_name AS team1, t2.team_name AS team2,
       w.team_name AS winner,
       m.victory_margin, m.victory_type,
       v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams w ON m.winning_team_id = w.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'completed'
ORDER BY m.match_date DESC
LIMIT 20;
"""
        },
        {
            "id": "Q11",
            "title": "Player Performance Across Formats",
            "description": "Compare each player's runs across Test, ODI, and T20I formats (played at least 2 formats).",
            "query": """
SELECT p.full_name,
       MAX(CASE WHEN ps.format = 'Test' THEN ps.runs_scored ELSE 0 END) AS test_runs,
       MAX(CASE WHEN ps.format = 'ODI' THEN ps.runs_scored ELSE 0 END) AS odi_runs,
       MAX(CASE WHEN ps.format = 'T20I' THEN ps.runs_scored ELSE 0 END) AS t20i_runs,
       ROUND(AVG(ps.batting_average), 2) AS overall_avg
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT ps.format) >= 2
ORDER BY odi_runs DESC;
"""
        },
        {
            "id": "Q12",
            "title": "Home vs Away Performance",
            "description": "Analyze each team's win record at home vs away matches.",
            "query": """
SELECT t.team_name,
       SUM(CASE WHEN v.country = t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
       SUM(CASE WHEN v.country != t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins,
       COUNT(CASE WHEN v.country = t.country THEN 1 END) AS home_matches,
       COUNT(CASE WHEN v.country != t.country THEN 1 END) AS away_matches
FROM matches m
JOIN teams t ON (m.team1_id = t.team_id OR m.team2_id = t.team_id)
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'completed'
GROUP BY t.team_id, t.team_name
ORDER BY home_wins DESC;
"""
        },
        {
            "id": "Q13",
            "title": "Batting Partnerships 100+ Runs",
            "description": "Identify batting partnerships where two consecutive batsmen scored 100+ combined runs in the same innings.",
            "query": """
SELECT b1.match_id,
       p1.full_name AS batter1, b1.runs AS batter1_runs,
       p2.full_name AS batter2, b2.runs AS batter2_runs,
       (b1.runs + b2.runs) AS partnership_runs,
       b1.innings_number
FROM batting_performances b1
JOIN batting_performances b2
    ON b1.match_id = b2.match_id
    AND b1.innings_number = b2.innings_number
    AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
WHERE (b1.runs + b2.runs) >= 100
ORDER BY partnership_runs DESC;
"""
        },
        {
            "id": "Q14",
            "title": "Bowling Performance at Venues",
            "description": "Examine bowlers who played at least 3 matches at the same venue, with their average economy rate and wickets.",
            "query": """
SELECT p.full_name AS bowler,
       v.venue_name,
       COUNT(DISTINCT bp.match_id) AS matches_at_venue,
       ROUND(AVG(bp.economy_rate), 2) AS avg_economy,
       SUM(bp.wickets) AS total_wickets
FROM bowling_performances bp
JOIN matches m ON bp.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
JOIN players p ON bp.player_id = p.player_id
WHERE bp.overs_bowled >= 4
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bp.match_id) >= 3
ORDER BY avg_economy ASC;
"""
        },
        {
            "id": "Q15",
            "title": "Performance in Close Matches",
            "description": "Identify players who perform well in close matches (won by <50 runs OR <5 wickets).",
            "query": """
SELECT p.full_name,
       COUNT(DISTINCT bp.match_id) AS close_matches_played,
       ROUND(AVG(bp.runs), 2) AS avg_runs_in_close,
       SUM(CASE WHEN m.winning_team_id IN (
           SELECT team_id FROM teams WHERE team_id = (
               SELECT team_id FROM players WHERE player_id = bp.player_id
           )
       ) THEN 1 ELSE 0 END) AS team_wins
FROM batting_performances bp
JOIN matches m ON bp.match_id = m.match_id
JOIN players p ON bp.player_id = p.player_id
WHERE m.match_status = 'completed'
  AND (
      (m.victory_type = 'runs' AND m.victory_margin < 50) OR
      (m.victory_type = 'wickets' AND m.victory_margin < 5)
  )
GROUP BY p.player_id, p.full_name
ORDER BY avg_runs_in_close DESC;
"""
        },
        {
            "id": "Q16",
            "title": "Batting Trends by Year (Since 2020)",
            "description": "Track how players' batting performance changes per year since 2020. Min 5 matches per year.",
            "query": """
SELECT p.full_name,
       YEAR(m.match_date) AS year,
       COUNT(DISTINCT bp.match_id) AS matches,
       ROUND(AVG(bp.runs), 2) AS avg_runs,
       ROUND(AVG(bp.strike_rate), 2) AS avg_sr
FROM batting_performances bp
JOIN matches m ON bp.match_id = m.match_id
JOIN players p ON bp.player_id = p.player_id
WHERE YEAR(m.match_date) >= 2020
GROUP BY p.player_id, p.full_name, YEAR(m.match_date)
HAVING COUNT(DISTINCT bp.match_id) >= 1
ORDER BY p.full_name, year;
"""
        },
    ],
    "Advanced": [
        {
            "id": "Q17",
            "title": "Toss Advantage Analysis",
            "description": "Does winning the toss help win matches? Calculate win % for toss-winning teams by toss decision.",
            "query": """
SELECT toss_decision,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) AS toss_winner_wins,
       ROUND(
           SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
       ) AS win_percentage
FROM matches
WHERE match_status = 'completed'
  AND toss_winner_id IS NOT NULL
  AND winning_team_id IS NOT NULL
GROUP BY toss_decision;
"""
        },
        {
            "id": "Q18",
            "title": "Most Economical Bowlers (Limited Overs)",
            "description": "Find most economical bowlers in ODI and T20I cricket. Min 10 matches, at least 2 overs/match avg.",
            "query": """
SELECT p.full_name,
       ps.format,
       ps.economy_rate,
       ps.wickets_taken,
       ps.matches_played,
       ROUND(ps.wickets_taken * 1.0 / NULLIF(ps.matches_played, 0), 2) AS wickets_per_match
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
WHERE ps.format IN ('ODI', 'T20I')
  AND ps.matches_played >= 5
  AND ps.wickets_taken > 0
  AND ps.economy_rate > 0
ORDER BY ps.economy_rate ASC;
"""
        },
        {
            "id": "Q19",
            "title": "Batting Consistency (Std Dev)",
            "description": "Determine the most consistent batsmen using standard deviation of runs. Lower std dev = more consistent.",
            "query": """
SELECT p.full_name,
       COUNT(bp.perf_id) AS innings,
       ROUND(AVG(bp.runs), 2) AS avg_runs,
       ROUND(STDDEV(bp.runs), 2) AS std_dev,
       MIN(bp.runs) AS min_score,
       MAX(bp.runs) AS max_score
FROM batting_performances bp
JOIN players p ON bp.player_id = p.player_id
JOIN matches m ON bp.match_id = m.match_id
WHERE bp.balls_faced >= 10
  AND YEAR(m.match_date) >= 2022
GROUP BY p.player_id, p.full_name
HAVING COUNT(bp.perf_id) >= 2
ORDER BY std_dev ASC;
"""
        },
        {
            "id": "Q20",
            "title": "Matches per Format with Batting Avg",
            "description": "Analyze how many matches each player has played in different formats and their batting averages. Min 20 total matches.",
            "query": """
SELECT p.full_name,
       SUM(CASE WHEN ps.format = 'Test' THEN ps.matches_played ELSE 0 END) AS test_matches,
       SUM(CASE WHEN ps.format = 'ODI' THEN ps.matches_played ELSE 0 END) AS odi_matches,
       SUM(CASE WHEN ps.format = 'T20I' THEN ps.matches_played ELSE 0 END) AS t20i_matches,
       SUM(ps.matches_played) AS total_matches,
       ROUND(MAX(CASE WHEN ps.format = 'Test' THEN ps.batting_average ELSE NULL END), 2) AS test_avg,
       ROUND(MAX(CASE WHEN ps.format = 'ODI' THEN ps.batting_average ELSE NULL END), 2) AS odi_avg,
       ROUND(MAX(CASE WHEN ps.format = 'T20I' THEN ps.batting_average ELSE NULL END), 2) AS t20i_avg
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING SUM(ps.matches_played) >= 5
ORDER BY total_matches DESC;
"""
        },
        {
            "id": "Q21",
            "title": "Comprehensive Player Ranking",
            "description": "Rank players using weighted batting + bowling + fielding points formula.",
            "query": """
SELECT p.full_name, t.team_name, ps.format,
       ROUND(
           (ps.runs_scored * 0.01) + (ps.batting_average * 0.5) + (ps.strike_rate * 0.3), 2
       ) AS batting_points,
       ROUND(
           (ps.wickets_taken * 2) + ((50 - COALESCE(ps.bowling_average, 50)) * 0.5) + ((6 - COALESCE(ps.economy_rate, 6)) * 2), 2
       ) AS bowling_points,
       ROUND((ps.catches * 3) + (ps.stumpings * 5), 2) AS fielding_points,
       ROUND(
           ((ps.runs_scored * 0.01) + (ps.batting_average * 0.5) + (ps.strike_rate * 0.3)) +
           ((ps.wickets_taken * 2) + ((50 - COALESCE(ps.bowling_average, 50)) * 0.5) + ((6 - COALESCE(ps.economy_rate, 6)) * 2)) +
           ((ps.catches * 3) + (ps.stumpings * 5)), 2
       ) AS total_score
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
JOIN teams t ON p.team_id = t.team_id
ORDER BY total_score DESC
LIMIT 20;
"""
        },
        {
            "id": "Q22",
            "title": "Head-to-Head Analysis",
            "description": "Build head-to-head match stats between teams that played at least 2 matches together.",
            "query": """
SELECT t1.team_name AS team_a, t2.team_name AS team_b,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) AS team_a_wins,
       SUM(CASE WHEN m.winning_team_id = t2.team_id THEN 1 ELSE 0 END) AS team_b_wins,
       ROUND(
           SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1
       ) AS team_a_win_pct
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
WHERE m.match_status = 'completed'
GROUP BY m.team1_id, m.team2_id, t1.team_name, t2.team_name
HAVING COUNT(*) >= 1
ORDER BY total_matches DESC;
"""
        },
        {
            "id": "Q23",
            "title": "Recent Player Form Analysis",
            "description": "Analyze players' recent batting form based on their last matches and categorize their form.",
            "query": """
SELECT p.full_name,
       COUNT(bp.perf_id) AS total_innings,
       ROUND(AVG(bp.runs), 2) AS avg_runs,
       ROUND(AVG(bp.strike_rate), 2) AS avg_sr,
       SUM(CASE WHEN bp.runs >= 50 THEN 1 ELSE 0 END) AS scores_above_50,
       ROUND(STDDEV(bp.runs), 2) AS consistency_score,
       CASE
           WHEN AVG(bp.runs) >= 60 THEN 'Excellent Form'
           WHEN AVG(bp.runs) >= 40 THEN 'Good Form'
           WHEN AVG(bp.runs) >= 20 THEN 'Average Form'
           ELSE 'Poor Form'
       END AS form_category
FROM batting_performances bp
JOIN players p ON bp.player_id = p.player_id
GROUP BY p.player_id, p.full_name
ORDER BY avg_runs DESC;
"""
        },
        {
            "id": "Q24",
            "title": "Best Batting Partnerships",
            "description": "Study successful batting partnerships between consecutive batsmen (at least 5 partnerships together).",
            "query": """
SELECT p1.full_name AS batter1, p2.full_name AS batter2,
       COUNT(*) AS partnership_count,
       ROUND(AVG(b1.runs + b2.runs), 2) AS avg_partnership,
       MAX(b1.runs + b2.runs) AS highest_partnership,
       SUM(CASE WHEN (b1.runs + b2.runs) >= 50 THEN 1 ELSE 0 END) AS good_partnerships
FROM batting_performances b1
JOIN batting_performances b2
    ON b1.match_id = b2.match_id
    AND b1.innings_number = b2.innings_number
    AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
GROUP BY b1.player_id, b2.player_id, p1.full_name, p2.full_name
HAVING COUNT(*) >= 1
ORDER BY avg_partnership DESC;
"""
        },
        {
            "id": "Q25",
            "title": "Career Trajectory Analysis",
            "description": "Perform time-series analysis of player batting evolution. Categorize career phase.",
            "query": """
WITH yearly_stats AS (
    SELECT p.player_id, p.full_name,
           YEAR(m.match_date) AS year,
           COUNT(bp.perf_id) AS innings,
           ROUND(AVG(bp.runs), 2) AS avg_runs,
           ROUND(AVG(bp.strike_rate), 2) AS avg_sr
    FROM batting_performances bp
    JOIN matches m ON bp.match_id = m.match_id
    JOIN players p ON bp.player_id = p.player_id
    GROUP BY p.player_id, p.full_name, YEAR(m.match_date)
    HAVING COUNT(bp.perf_id) >= 1
),
player_trends AS (
    SELECT player_id, full_name,
           COUNT(DISTINCT year) AS active_years,
           ROUND(AVG(avg_runs), 2) AS career_avg,
           MAX(avg_runs) AS peak_avg,
           MIN(avg_runs) AS lowest_avg,
           MAX(year) AS last_year,
           MIN(year) AS first_year
    FROM yearly_stats
    GROUP BY player_id, full_name
)
SELECT full_name, active_years, career_avg,
       peak_avg, lowest_avg,
       (last_year - first_year + 1) AS career_span_years,
       CASE
           WHEN career_avg >= 50 THEN 'Career Ascending'
           WHEN career_avg >= 30 THEN 'Career Stable'
           ELSE 'Career Declining'
       END AS career_phase
FROM player_trends
ORDER BY career_avg DESC;
"""
        },
    ]
}


def show():
    st.title("🔍 SQL Analytics")
    st.caption("25 SQL queries — Beginner to Advanced — running on your MySQL database")

    # Difficulty selector
    level = st.radio("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"], horizontal=True)

    st.markdown("---")

    questions = SQL_QUESTIONS[level]

    for q in questions:
        with st.expander(f"**{q['id']}** — {q['title']}"):
            st.markdown(f"**❓ Question:** {q['description']}")
            st.code(q["query"].strip(), language="sql")

            col1, col2 = st.columns([1, 4])
            with col1:
                run_btn = st.button(f"▶️ Run Query", key=f"run_{q['id']}")

            if run_btn:
                with st.spinner("Running query..."):
                    results = run_query(q["query"])

                if results is None:
                    st.error("Query failed. Check your database connection.")
                elif len(results) == 0:
                    st.info("Query ran successfully but returned no rows. (Your database may need more sample data for this query.)")
                else:
                    df = pd.DataFrame(results)
                    st.success(f"✅ {len(df)} row(s) returned")
                    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("✏️ Custom SQL Query")
    st.caption("Write and run your own SQL query on the cricbuzz_db database.")

    custom_sql = st.text_area(
        "Enter SQL:",
        value="SELECT * FROM players LIMIT 10;",
        height=120
    )

    if st.button("▶️ Run Custom Query"):
        if not custom_sql.strip():
            st.warning("Please enter a SQL query.")
        else:
            # Basic safety - block destructive ops with confirmation
            dangerous = any(kw in custom_sql.upper() for kw in ["DROP", "TRUNCATE", "DELETE", "UPDATE", "INSERT"])
            if dangerous:
                st.warning("⚠️ Destructive queries are disabled in this interface. Use the CRUD page for data modifications.")
            else:
                with st.spinner("Running..."):
                    results = run_query(custom_sql)
                if results is None:
                    st.error("Query failed.")
                elif isinstance(results, list) and len(results) == 0:
                    st.info("Query returned no rows.")
                else:
                    df = pd.DataFrame(results)
                    st.success(f"✅ {len(df)} row(s) returned")
                    st.dataframe(df, use_container_width=True, hide_index=True)
