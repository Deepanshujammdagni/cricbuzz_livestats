"""
Fetches and displays live/recent cricket match data from Cricbuzz API via RapidAPI.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")

BASE_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}


def fetch_api(endpoint):
    """Generic API fetch with error handling."""
    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_rapidapi_key_here":
        return None, "API key not configured. Please add RAPIDAPI_KEY to your .env file."
    try:
        url = f"https://{RAPIDAPI_HOST}/{endpoint}"
        response = requests.get(url, headers=BASE_HEADERS, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, "Request timed out. Check your internet connection."
    except requests.exceptions.HTTPError as e:
        return None, f"API error: {e.response.status_code} - {e.response.text[:200]}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def show_match_card(match):
    """Renders a single match card."""
    try:
        desc = match.get("matchDesc", "Match")
        series = match.get("seriesName", "")
        status = match.get("status", "")
        state = match.get("state", "")

        # Team info
        team1 = match.get("team1", {})
        team2 = match.get("team2", {})
        t1_name = team1.get("teamName", "Team 1")
        t2_name = team2.get("teamName", "Team 2")
        t1_score = team1.get("teamScore", {})
        t2_score = team2.get("teamScore", {})

        # Score formatting
        def fmt_score(score_dict):
            if not score_dict:
                return "Yet to bat"
            parts = []
            for key in ["inngs1", "inngs2"]:
                inns = score_dict.get(key)
                if inns:
                    r = inns.get("runs", 0)
                    w = inns.get("wickets", "")
                    o = inns.get("overs", "")
                    if w == 10:
                        parts.append(f"{r} ({o} ov)")
                    elif w:
                        parts.append(f"{r}/{w} ({o} ov)")
                    else:
                        parts.append(str(r))
            return " & ".join(parts) if parts else "Yet to bat"

        t1_score_str = fmt_score(t1_score)
        t2_score_str = fmt_score(t2_score)

        # Status badge color
        state_color = {"complete": "🟢", "inprogress": "🔴", "preview": "🔵"}.get(state.lower(), "⚪")

        with st.container():
            st.markdown(f"""
            <div style="background:#1e1b4b; border-radius:10px; padding:1rem 1.2rem; margin-bottom:0.8rem; border-left: 4px solid {'#ef4444' if state.lower()=='inprogress' else '#6366f1'}">
                <div style="color:#a5b4fc; font-size:0.75rem; margin-bottom:0.3rem">{series} — {desc}</div>
                <div style="display:flex; justify-content:space-between; align-items:center">
                    <div>
                        <div style="color:white; font-size:1rem; font-weight:700">{t1_name}</div>
                        <div style="color:#f97316; font-size:0.95rem">{t1_score_str}</div>
                    </div>
                    <div style="color:#6b7280; font-size:1.2rem; font-weight:bold">vs</div>
                    <div style="text-align:right">
                        <div style="color:white; font-size:1rem; font-weight:700">{t2_name}</div>
                        <div style="color:#f97316; font-size:0.95rem">{t2_score_str}</div>
                    </div>
                </div>
                <div style="color:#9ca3af; font-size:0.8rem; margin-top:0.5rem">{state_color} {status}</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not render match card: {e}")


def show():
    st.title("📡 Live Matches")
    st.caption("Powered by Cricbuzz API via RapidAPI")

    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_rapidapi_key_here":
        st.warning("""
        ⚠️ **API Key Not Configured**

        To see live matches, add your RapidAPI key to `.env`:
        ```
        RAPIDAPI_KEY=your_key_here
        ```
        Get a free key at [RapidAPI - Cricbuzz Cricket](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket)
        """)

        st.info("📋 Showing demo/cached data instead:")
        _show_demo_matches()
        return

    tab1, tab2, tab3 = st.tabs(["🔴 Live", "✅ Recent", "🔵 Upcoming"])

    with tab1:
        st.subheader("Live Matches")
        with st.spinner("Fetching live matches..."):
            data, err = fetch_api("matches/v1/live")
        if err:
            st.error(err)
        elif data:
            matches = []
            for type_match in data.get("typeMatches", []):
                for series_match in type_match.get("seriesMatches", []):
                    sm = series_match.get("seriesAdWrapper", {})
                    for m in sm.get("matches", []):
                        matches.append(m.get("matchInfo", {}))

            if matches:
                for m in matches:
                    show_match_card(m)
            else:
                st.info("No live matches right now. Check the Recent tab!")

    with tab2:
        st.subheader("Recent Matches")
        with st.spinner("Fetching recent matches..."):
            data, err = fetch_api("matches/v1/recent")
        if err:
            st.error(err)
        elif data:
            matches = []
            for type_match in data.get("typeMatches", []):
                for series_match in type_match.get("seriesMatches", []):
                    sm = series_match.get("seriesAdWrapper", {})
                    for m in sm.get("matches", []):
                        matches.append(m.get("matchInfo", {}))

            if matches:
                for m in matches[:15]:  # limit to 15
                    show_match_card(m)
            else:
                st.info("No recent matches found.")

    with tab3:
        st.subheader("Upcoming Matches")
        with st.spinner("Fetching upcoming matches..."):
            data, err = fetch_api("matches/v1/upcoming")
        if err:
            st.error(err)
        elif data:
            matches = []
            for type_match in data.get("typeMatches", []):
                for series_match in type_match.get("seriesMatches", []):
                    sm = series_match.get("seriesAdWrapper", {})
                    for m in sm.get("matches", []):
                        matches.append(m.get("matchInfo", {}))

            if matches:
                for m in matches[:15]:
                    show_match_card(m)
            else:
                st.info("No upcoming matches found.")


def _show_demo_matches():
    """Demo data when API key is not configured."""
    demo = [
        {
            "matchDesc": "3rd ODI",
            "seriesName": "India vs Australia ODI Series",
            "state": "inprogress",
            "status": "India needs 45 runs from 30 balls",
            "team1": {"teamName": "India", "teamScore": {"inngs1": {"runs": 287, "wickets": 6, "overs": "44.3"}}},
            "team2": {"teamName": "Australia", "teamScore": {"inngs1": {"runs": 310, "wickets": 10, "overs": "50.0"}}},
        },
        {
            "matchDesc": "2nd Test, Day 3",
            "seriesName": "Border-Gavaskar Trophy",
            "state": "inprogress",
            "status": "Australia trail by 156 runs",
            "team1": {"teamName": "India", "teamScore": {"inngs1": {"runs": 487, "wickets": 10, "overs": "152.2"}}},
            "team2": {"teamName": "Australia", "teamScore": {"inngs1": {"runs": 215, "wickets": 6, "overs": "67.0"}}},
        },
        {
            "matchDesc": "1st T20I",
            "seriesName": "Pakistan vs England T20 Series",
            "state": "complete",
            "status": "England won by 5 wickets",
            "team1": {"teamName": "Pakistan", "teamScore": {"inngs1": {"runs": 168, "wickets": 9, "overs": "20.0"}}},
            "team2": {"teamName": "England", "teamScore": {"inngs1": {"runs": 172, "wickets": 5, "overs": "18.4"}}},
        },
    ]
    for m in demo:
        show_match_card(m)
