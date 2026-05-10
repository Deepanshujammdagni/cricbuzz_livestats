"""
Home page - Project overview and navigation
"""

import streamlit as st


def show():
    st.markdown("""
    <style>
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f97316, #ef4444, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .hero-sub {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-top: 0.3rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #f97316;
        color: white;
        margin-bottom: 1rem;
    }
    .badge {
        background: #f97316;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 0.3rem;
    }
    .tech-pill {
        display: inline-block;
        background: #312e81;
        color: #a5b4fc;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-title">🏏 Cricbuzz LiveStats</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Real-Time Cricket Insights & SQL-Based Analytics Dashboard</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📡 Pages", "5")
    col2.metric("🗄️ SQL Queries", "25+")
    col3.metric("🏏 Sample Players", "20+")
    col4.metric("📅 Sample Matches", "10+")

    st.markdown("---")

    st.subheader("📖 About the Project")
    st.write("""
    **Cricbuzz LiveStats** is a cricket analytics platform that combines live data from the
    Cricbuzz API with a MySQL database to power interactive analytics and CRUD operations.

    It was built as a learning project covering:
    - REST API integration using Python `requests`
    - MySQL database design and query optimization
    - Interactive dashboards with Streamlit
    - Full CRUD operations via a form-based UI
    """)

    st.subheader("🗂️ Project Structure")
    st.code("""
cricbuzz_livestats/
├── app.py                  # Main Streamlit entry point
├── requirements.txt        # Python dependencies
├── schema.sql              # MySQL schema + sample data
├── .env.example            # Environment variable template
│
├── app_pages/
│   ├── home.py             # This page
│   ├── live_matches.py     # Live match data from Cricbuzz API
│   ├── top_stats.py        # Top batting/bowling stats
│   ├── sql_queries.py      # 25 SQL queries interface
│   └── crud_operations.py  # CRUD on players/matches
│
└── utils/
    └── db_connection.py    # MySQL connection handler
    """, language="text")

    st.subheader("🛠️ Tech Stack")
    techs = ["Python 3.10+", "Streamlit", "MySQL", "REST API (Cricbuzz via RapidAPI)",
             "pandas", "plotly", "mysql-connector-python", "python-dotenv"]
    pills = " ".join([f'<span class="tech-pill">{t}</span>' for t in techs])
    st.markdown(pills, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Pages Overview")

    pages_info = [
        ("📡 Live Matches", "Real-time match data from Cricbuzz API. View ongoing, recent, and upcoming matches with full scorecard details."),
        ("📊 Top Stats", "Top batting and bowling stats fetched live. View most runs, highest scores, most wickets, and more."),
        ("🔍 SQL Analytics", "25 hand-written SQL queries from beginner to advanced. Run them against the MySQL database interactively."),
        ("🛠️ CRUD Operations", "Add, view, update, and delete player records directly in MySQL. Good for learning database operations."),
    ]

    for title, desc in pages_info:
        st.markdown(f"""
        <div class="feature-card">
            <strong>{title}</strong><br>
            <span style="color: #c7d2fe; font-size: 0.9rem;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚙️ Setup Instructions")
    st.markdown("""
    **1. Clone the repo and install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    **2. Set up MySQL database:**
    ```bash
    mysql -u root -p < schema.sql
    ```

    **3. Configure environment variables:**
    ```bash
    cp .env.example .env
    # Edit .env with your MySQL credentials and RapidAPI key
    ```

    **4. Run the app:**
    ```bash
    streamlit run app.py
    ```
    """)

    st.info("💡 **Tip:** Get a free Cricbuzz API key from [RapidAPI](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket) to power the live pages.")
