"""
app.py - Main Streamlit entry point for Cricbuzz LiveStats
Run with: streamlit run app.py
"""

import streamlit as st
from utils.db_connection import test_connection

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - makes it look nice without being over the top
st.markdown("""
<style>
    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Main background */
    .main {
        background-color: #e2e8f0;
    }

    /* Remove default Streamlit padding a bit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #1e1b4b;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        border-left: 3px solid #f97316;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e1b4b;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a5b4fc;
        border-radius: 6px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f97316 !important;
        color: white !important;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid #312e81;
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #f97316, #ef4444);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover {
        opacity: 0.85;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e1b4b !important;
        border-radius: 8px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar Navigation ----
with st.sidebar:
    st.markdown("## 🏏 Cricbuzz LiveStats")
    st.markdown("---")

    pages = {
        "🏠 Home": "home",
        "📡 Live Matches": "live_matches",
        "📊 Top Stats": "top_stats",
        "🔍 SQL Analytics": "sql_queries",
        "🛠️ CRUD Operations": "crud_operations",
    }

    selected_page = st.radio("Navigate", list(pages.keys()), label_visibility="collapsed")

    st.markdown("---")

    # DB connection status indicator
    st.markdown("### 🗄️ Database Status")
    db_ok = test_connection()
    if db_ok:
        st.success("✅ MySQL Connected")
    else:
        st.error("❌ MySQL Not Connected")
        st.caption("Check your .env file with DB credentials.")

    st.markdown("---")
    st.caption("Built with Python · Streamlit · MySQL · Cricbuzz API")
    st.caption("v1.0 — Sports Analytics Project")

# ---- Page Routing ----
page_key = pages[selected_page]

if page_key == "home":
    from pages import home
    home.show()

elif page_key == "live_matches":
    from pages import live_matches
    live_matches.show()

elif page_key == "top_stats":
    from pages import top_stats
    top_stats.show()

elif page_key == "sql_queries":
    from pages import sql_queries
    sql_queries.show()

elif page_key == "crud_operations":
    from pages import crud_operations
    crud_operations.show()
