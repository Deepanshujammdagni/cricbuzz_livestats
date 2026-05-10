"""
Displays top batting and bowling statistics.
Tries Cricbuzz API first, falls back to MySQL database stats.
"""

import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from utils.db_connection import run_query
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")


def fetch_api(endpoint):
    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_rapidapi_key_here":
        return None, "No API key"
    try:
        url = f"https://{RAPIDAPI_HOST}/{endpoint}"
        headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def show_batting_from_db(fmt):
    """Fetch top batting stats from MySQL."""
    q = """
        SELECT p.full_name AS Player, t.team_name AS Team,
               ps.matches_played AS M, ps.innings AS Inn,
               ps.runs_scored AS Runs, ps.highest_score AS HS,
               ps.batting_average AS Avg, ps.strike_rate AS SR,
               ps.centuries AS `100s`, ps.half_centuries AS `50s`
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        JOIN teams t ON p.team_id = t.team_id
        WHERE ps.format = %s AND ps.runs_scored > 0
        ORDER BY ps.runs_scored DESC
        LIMIT 15
    """
    results = run_query(q, (fmt,))
    return pd.DataFrame(results) if results else pd.DataFrame()


def show_bowling_from_db(fmt):
    """Fetch top bowling stats from MySQL."""
    q = """
        SELECT p.full_name AS Player, t.team_name AS Team,
               ps.matches_played AS M,
               ps.wickets_taken AS Wkts,
               ps.bowling_average AS Avg,
               ps.economy_rate AS Econ
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        JOIN teams t ON p.team_id = t.team_id
        WHERE ps.format = %s AND ps.wickets_taken > 0
        ORDER BY ps.wickets_taken DESC
        LIMIT 15
    """
    results = run_query(q, (fmt,))
    return pd.DataFrame(results) if results else pd.DataFrame()


def show():
    st.title("📊 Top Player Stats")
    st.caption("Live stats from Cricbuzz API + MySQL database fallback")

    format_opts = {"ODI": "ODI", "Test": "Test", "T20I": "T20I"}
    selected_fmt = st.selectbox("Select Format", list(format_opts.keys()), key="stats_fmt")

    tab1, tab2 = st.tabs(["🏏 Top Batters", "🎯 Top Bowlers"])

    with tab1:
        st.subheader(f"Top {selected_fmt} Batters")

        # Try API first
        api_used = False
        if RAPIDAPI_KEY and RAPIDAPI_KEY != "your_rapidapi_key_here":
            fmt_map = {"ODI": "odi", "Test": "test", "T20I": "t20i"}
            data, err = fetch_api(f"stats/v1/rankings/batsmen?formatType={fmt_map[selected_fmt]}")
            if data and not err:
                try:
                    ranks = data.get("rank", [])[:15]
                    rows = []
                    for r in ranks:
                        rows.append({
                            "Rank": r.get("rank", ""),
                            "Player": r.get("name", ""),
                            "Country": r.get("country", ""),
                            "Rating": r.get("rating", ""),
                        })
                    if rows:
                        df = pd.DataFrame(rows)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        api_used = True
                        st.caption("✅ Data from Cricbuzz API (ICC Rankings)")
                except Exception:
                    pass

        if not api_used:
            st.caption("📦 Showing data from MySQL database")
            df = show_batting_from_db(selected_fmt)
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Bar chart - Top 10 run scorers
                chart_df = df.head(10)
                fig = px.bar(
                    chart_df, x="Player", y="Runs",
                    title=f"Top 10 {selected_fmt} Run Scorers",
                    color="Runs",
                    color_continuous_scale="oranges",
                    text="Runs"
                )
                fig.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    font_color="white",
                    xaxis_tickangle=-30,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

                # Centuries chart
                fig2 = px.bar(
                    chart_df, x="Player", y="100s",
                    title=f"Centuries in {selected_fmt}",
                    color="100s",
                    color_continuous_scale="reds",
                    text="100s"
                )
                fig2.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    font_color="white",
                    xaxis_tickangle=-30,
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No batting data found in database for this format.")

    with tab2:
        st.subheader(f"Top {selected_fmt} Bowlers")

        api_used = False
        if RAPIDAPI_KEY and RAPIDAPI_KEY != "your_rapidapi_key_here":
            fmt_map = {"ODI": "odi", "Test": "test", "T20I": "t20i"}
            data, err = fetch_api(f"stats/v1/rankings/bowlers?formatType={fmt_map[selected_fmt]}")
            if data and not err:
                try:
                    ranks = data.get("rank", [])[:15]
                    rows = []
                    for r in ranks:
                        rows.append({
                            "Rank": r.get("rank", ""),
                            "Player": r.get("name", ""),
                            "Country": r.get("country", ""),
                            "Rating": r.get("rating", ""),
                        })
                    if rows:
                        df = pd.DataFrame(rows)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        api_used = True
                        st.caption("✅ Data from Cricbuzz API (ICC Rankings)")
                except Exception:
                    pass

        if not api_used:
            st.caption("📦 Showing data from MySQL database")
            df = show_bowling_from_db(selected_fmt)
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)

                chart_df = df.head(10)
                fig = px.bar(
                    chart_df, x="Player", y="Wkts",
                    title=f"Top 10 {selected_fmt} Wicket Takers",
                    color="Wkts",
                    color_continuous_scale="purples",
                    text="Wkts"
                )
                fig.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    font_color="white",
                    xaxis_tickangle=-30,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

                fig2 = px.scatter(
                    df, x="Econ", y="Avg",
                    hover_name="Player",
                    title="Economy Rate vs Bowling Average",
                    color="Wkts",
                    color_continuous_scale="plasma",
                    size="Wkts"
                )
                fig2.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    font_color="white"
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No bowling data found in database for this format.")

    # Summary stats from DB
    st.markdown("---")
    st.subheader("🗄️ Database Summary")
    col1, col2, col3, col4 = st.columns(4)

    player_count = run_query("SELECT COUNT(*) AS c FROM players")
    match_count = run_query("SELECT COUNT(*) AS c FROM matches")
    team_count = run_query("SELECT COUNT(*) AS c FROM teams")
    venue_count = run_query("SELECT COUNT(*) AS c FROM venues")

    col1.metric("👤 Players", player_count[0]["c"] if player_count else "N/A")
    col2.metric("🏟️ Matches", match_count[0]["c"] if match_count else "N/A")
    col3.metric("🚩 Teams", team_count[0]["c"] if team_count else "N/A")
    col4.metric("🏟️ Venues", venue_count[0]["c"] if venue_count else "N/A")
