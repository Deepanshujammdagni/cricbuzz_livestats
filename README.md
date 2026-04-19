# 🏏 Cricbuzz LiveStats

**Real-Time Cricket Insights & SQL-Based Analytics Dashboard**

Built with Python, Streamlit, MySQL, and the Cricbuzz API via RapidAPI.

---

## 📦 Project Structure

```
cricbuzz_livestats/
├── app.py                  # Main Streamlit entry point
├── requirements.txt        # Python dependencies
├── schema.sql              # MySQL schema + sample data
├── .env.example            # Environment variable template
│
├── pages/
│   ├── home.py             # Project overview and navigation
│   ├── live_matches.py     # Live match data from Cricbuzz API
│   ├── top_stats.py        # Top batting/bowling stats
│   ├── sql_queries.py      # 25 SQL queries interface
│   └── crud_operations.py  # CRUD on players/matches
│
└── utils/
    └── db_connection.py    # MySQL connection handler
```

---

## ⚙️ Setup Instructions

### 1. Create environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MySQL database

Make sure MySQL is running on your machine, then:

```bash
net start MySQL80
mysql -u root -p < schema.sql
```

This creates the `cricbuzz_db` database with all tables and sample data.

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:

- Your MySQL host, port, user, password
- Your RapidAPI key (for live Cricbuzz data)

```
RAPIDAPI_KEY=your_key_here
RAPIDAPI_HOST=cricbuzz-cricket.p.rapidapi.com
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=cricbuzz_db
```

Get a free Cricbuzz API key at: https://rapidapi.com/cricketapilive/api/cricbuzz-cricket

### 4. Run the app

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## 🗄️ Database Schema

| Table                  | Description                                  |
| ---------------------- | -------------------------------------------- |
| `teams`                | Cricket teams (India, Australia, etc.)       |
| `players`              | Player info with role, batting/bowling style |
| `venues`               | Cricket grounds with city, country, capacity |
| `series`               | Cricket series/tournaments                   |
| `matches`              | Match records with results                   |
| `player_stats`         | Career stats per player per format           |
| `batting_performances` | Per-match batting records                    |
| `bowling_performances` | Per-match bowling records                    |

---

## 📄 Pages

| Page             | Description                                |
| ---------------- | ------------------------------------------ |
| 🏠 Home          | Project info and setup guide               |
| 📡 Live Matches  | Live, recent, and upcoming matches via API |
| 📊 Top Stats     | Top batters/bowlers from API + DB charts   |
| 🔍 SQL Analytics | 25 SQL queries (Easy/Medium/Hard)          |
| 🛠️ CRUD          | Add/View/Update/Delete players             |

---

## 🧑‍💻 Tech Stack

- **Python 3.10+**
- **Streamlit** — web UI
- **MySQL** — relational database
- **mysql-connector-python** — DB driver
- **requests** — API calls
- **pandas** — data manipulation
- **plotly** — charts and visualizations
- **python-dotenv** — environment variable management

---

## 📋 Notes

- The app works with or without a Cricbuzz API key. Without a key, live match pages show demo data.
- All SQL queries (Q1–Q25) run against the MySQL database.
- Sample data is included in `schema.sql` so you can test everything locally.

---
