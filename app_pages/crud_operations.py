"""
Full Create, Read, Update, Delete operations on the players table.

"""

import streamlit as st
import pandas as pd
from utils.db_connection import run_querys


def get_teams():
    """Returns list of teams for dropdown selection."""
    teams = run_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
    if teams:
        return {t["team_name"]: t["team_id"] for t in teams}
    return {}


def show():
    st.title("🛠️ CRUD Operations")
    st.caption("Create, Read, Update, Delete player records in MySQL")

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Player", "👀 View Players", "✏️ Update Player", "🗑️ Delete Player"])

    teams = get_teams()
    team_names = list(teams.keys())

    # -------- CREATE --------
    with tab1:
        st.subheader("➕ Add New Player")
        with st.form("add_player_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", placeholder="e.g., Yashasvi Jaiswal")
                team_name = st.selectbox("Team *", team_names if team_names else ["(No teams found)"])
                playing_role = st.selectbox("Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                dob = st.date_input("Date of Birth")
            with col2:
                batting_style = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
                bowling_style = st.text_input("Bowling Style", placeholder="e.g., Right-arm fast")
                nationality = st.text_input("Nationality", placeholder="e.g., Indian")

            submitted = st.form_submit_button("✅ Add Player")

            if submitted:
                if not full_name.strip():
                    st.error("Full Name is required!")
                elif not team_names:
                    st.error("No teams available in database. Please check database connection.")
                else:
                    team_id = teams.get(team_name)
                    q = """
                        INSERT INTO players (full_name, team_id, playing_role, batting_style, bowling_style, date_of_birth, nationality)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    result = run_query(q, (full_name.strip(), team_id, playing_role, batting_style,
                                          bowling_style.strip(), dob, nationality.strip()), fetch=False)
                    if result is not None and result > 0:
                        st.success(f"✅ Player **{full_name}** added successfully!")
                    else:
                        st.error("Failed to add player. Check DB connection.")

    # -------- READ --------
    with tab2:
        st.subheader("👀 View All Players")

        col1, col2 = st.columns([2, 2])
        with col1:
            search_name = st.text_input("🔍 Search by name", placeholder="e.g., Kohli")
        with col2:
            filter_role = st.selectbox("Filter by role", ["All", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])

        q = """
            SELECT p.player_id AS ID, p.full_name AS Name, t.team_name AS Team,
                   p.playing_role AS Role, p.batting_style AS `Batting Style`,
                   p.bowling_style AS `Bowling Style`, p.nationality AS Nationality,
                   p.date_of_birth AS DOB
            FROM players p
            LEFT JOIN teams t ON p.team_id = t.team_id
            WHERE 1=1
        """
        params = []

        if search_name.strip():
            q += " AND p.full_name LIKE %s"
            params.append(f"%{search_name.strip()}%")

        if filter_role != "All":
            q += " AND p.playing_role = %s"
            params.append(filter_role)

        q += " ORDER BY p.full_name"

        results = run_query(q, params if params else None)

        if results:
            df = pd.DataFrame(results)
            st.success(f"Found {len(df)} player(s)")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Pie chart of roles
            role_counts = df["Role"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]

            import plotly.express as px
            fig = px.pie(role_counts, names="Role", values="Count", title="Players by Role",
                         color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(paper_bgcolor="#0f172a", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No players found.")

    # -------- UPDATE --------
    with tab3:
        st.subheader("✏️ Update Player")

        # Fetch all players for selection
        players = run_query("SELECT player_id, full_name FROM players ORDER BY full_name")
        if not players:
            st.warning("No players in database.")
        else:
            player_map = {f"{p['full_name']} (ID: {p['player_id']})": p['player_id'] for p in players}
            selected_label = st.selectbox("Select Player to Update", list(player_map.keys()))
            selected_id = player_map[selected_label]

            # Fetch current data
            current = run_query("SELECT * FROM players WHERE player_id = %s", (selected_id,))
            if current:
                c = current[0]
                with st.form("update_player_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Full Name", value=c.get("full_name", ""))
                        current_team = run_query("SELECT team_name FROM teams WHERE team_id = %s", (c.get("team_id"),))
                        current_team_name = current_team[0]["team_name"] if current_team else (team_names[0] if team_names else "")
                        default_idx = team_names.index(current_team_name) if current_team_name in team_names else 0
                        new_team = st.selectbox("Team", team_names, index=default_idx)
                        role_list = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                        current_role = c.get("playing_role", "Batsman")
                        role_idx = role_list.index(current_role) if current_role in role_list else 0
                        new_role = st.selectbox("Playing Role", role_list, index=role_idx)
                    with col2:
                        bat_list = ["Right-hand bat", "Left-hand bat"]
                        current_bat = c.get("batting_style", "Right-hand bat")
                        bat_idx = bat_list.index(current_bat) if current_bat in bat_list else 0
                        new_bat = st.selectbox("Batting Style", bat_list, index=bat_idx)
                        new_bowl = st.text_input("Bowling Style", value=c.get("bowling_style", "") or "")
                        new_nat = st.text_input("Nationality", value=c.get("nationality", "") or "")

                    update_btn = st.form_submit_button("💾 Update Player")

                    if update_btn:
                        new_team_id = teams.get(new_team)
                        q = """
                            UPDATE players
                            SET full_name=%s, team_id=%s, playing_role=%s,
                                batting_style=%s, bowling_style=%s, nationality=%s
                            WHERE player_id=%s
                        """
                        result = run_query(q, (new_name, new_team_id, new_role, new_bat,
                                               new_bowl, new_nat, selected_id), fetch=False)
                        if result is not None and result > 0:
                            st.success(f"✅ Player updated successfully!")
                        else:
                            st.error("Update failed.")

    # -------- DELETE --------
    with tab4:
        st.subheader("🗑️ Delete Player")
        st.warning("⚠️ This action is **permanent** and cannot be undone.")

        players = run_query("SELECT player_id, full_name, playing_role FROM players ORDER BY full_name")
        if not players:
            st.info("No players in database.")
        else:
            player_map2 = {f"{p['full_name']} ({p['playing_role']}) — ID: {p['player_id']}": p['player_id'] for p in players}
            del_label = st.selectbox("Select Player to Delete", list(player_map2.keys()), key="del_select")
            del_id = player_map2[del_label]

            st.info(f"You are about to delete: **{del_label}**")

            col1, col2 = st.columns([1, 5])
            with col1:
                confirm = st.checkbox("I confirm deletion")
            with col2:
                del_btn = st.button("🗑️ Delete Player", disabled=not confirm)

            if del_btn and confirm:
                result = run_query("DELETE FROM players WHERE player_id = %s", (del_id,), fetch=False)
                if result is not None and result > 0:
                    st.success("✅ Player deleted successfully!")
                    st.rerun()
                else:
                    st.error("Deletion failed.")

    # -------- Match CRUD Section --------
    st.markdown("---")
    st.subheader("🏏 View All Matches")
    matches = run_query("""
        SELECT m.match_id AS ID, m.match_description AS Description,
               t1.team_name AS Team1, t2.team_name AS Team2,
               m.match_format AS Format, m.match_date AS Date,
               m.match_status AS Status,
               w.team_name AS Winner,
               m.victory_margin AS Margin, m.victory_type AS VictoryType
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winning_team_id = w.team_id
        ORDER BY m.match_date DESC
    """)
    if matches:
        df = pd.DataFrame(matches)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No matches in database.")
