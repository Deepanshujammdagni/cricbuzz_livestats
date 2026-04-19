"""
check_setup.py
Run this FIRST to diagnose MySQL and API key issues before starting the app.

Usage:
    python check_setup.py
"""

import os
import sys

print("=" * 55)
print("  Cricbuzz LiveStats — Setup Checker")
print("=" * 55)

# ── 1. Check .env file ──────────────────────────────────────
print("\n[1] Checking .env file...")
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    print(f"    ✅ .env found at: {env_path}")
else:
    print(f"    ❌ .env NOT found at: {env_path}")
    print("    FIX: Copy .env.example to .env and fill in your values.")
    print("         In CMD:  copy .env.example .env")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv(env_path, override=True)

db_host = os.getenv("DB_HOST", "NOT SET")
db_port = os.getenv("DB_PORT", "NOT SET")
db_user = os.getenv("DB_USER", "NOT SET")
db_pass = os.getenv("DB_PASSWORD", "")
db_name = os.getenv("DB_NAME", "NOT SET")
api_key = os.getenv("RAPIDAPI_KEY", "")

print(f"    DB_HOST     = {db_host}")
print(f"    DB_PORT     = {db_port}")
print(f"    DB_USER     = {db_user}")
print(f"    DB_PASSWORD = {'(set)' if db_pass else '(EMPTY — this might be your problem!)'}")
print(f"    DB_NAME     = {db_name}")
print(f"    RAPIDAPI_KEY= {'(set)' if api_key and api_key != 'your_rapidapi_key_here' else '(NOT SET — live matches will show demo data)'}")

# ── 2. Check mysql-connector-python ────────────────────────
print("\n[2] Checking mysql-connector-python...")
try:
    import mysql.connector
    print(f"    ✅ mysql-connector-python installed (v{mysql.connector.__version__})")
except ImportError:
    print("    ❌ mysql-connector-python NOT installed")
    print("    FIX: pip install mysql-connector-python")
    sys.exit(1)

# ── 3. Check MySQL service is reachable ────────────────────
print("\n[3] Testing MySQL connection...")
try:
    conn = mysql.connector.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_pass,
        connection_timeout=8,
        use_pure=True,
    )
    print(f"    ✅ Connected to MySQL server at {db_host}:{db_port}")
    conn.close()
except mysql.connector.Error as e:
    errno = e.errno if hasattr(e, "errno") else 0
    print(f"    ❌ Connection failed (error {errno}): {e}")
    if errno == 2003:
        print("""
    FIX — MySQL service is not running. Try ONE of these:
    
    Option A — Start via Services UI:
        Press Win+R → type "services.msc" → Enter
        Find "MySQL80" (or MySQL57) → Right-click → Start
    
    Option B — Start via CMD (run as Administrator):
        net start MySQL80
    
    Option C — If you installed XAMPP:
        Open XAMPP Control Panel → Click Start next to MySQL
        
    Option D — Verify port isn't blocked:
        netstat -an | findstr 3306
        (should show a line with LISTENING)
""")
    elif errno == 1045:
        print("""
    FIX — Wrong username or password.
        - Open your .env file
        - Check DB_USER and DB_PASSWORD match your MySQL setup
        - If you never set a root password, try DB_PASSWORD=(leave empty)
        - Or connect with MySQL Workbench to confirm credentials
""")
    sys.exit(1)

# ── 4. Check if cricbuzz_db exists ─────────────────────────
print("\n[4] Checking database 'cricbuzz_db'...")
try:
    conn = mysql.connector.connect(
        host=db_host,
        port=int(db_port),
        user=db_user,
        password=db_pass,
        database=db_name,
        use_pure=True,
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    if tables:
        print(f"    ✅ Database '{db_name}' exists with tables: {', '.join(tables)}")
    else:
        print(f"    ⚠️  Database '{db_name}' exists but has NO tables yet.")
        print("    FIX: Run schema.sql to create tables and insert sample data:")
        print(f"         mysql -u {db_user} -p {db_name} < schema.sql")
except mysql.connector.Error as e:
    if e.errno == 1049:
        print(f"    ❌ Database '{db_name}' does not exist yet.")
        print("    FIX: Run this in CMD:")
        print(f"         mysql -u {db_user} -p < schema.sql")
    else:
        print(f"    ❌ Error: {e}")
    sys.exit(1)

# ── 5. Check streamlit ─────────────────────────────────────
print("\n[5] Checking Streamlit...")
try:
    import streamlit
    print(f"    ✅ Streamlit installed (v{streamlit.__version__})")
except ImportError:
    print("    ❌ Streamlit NOT installed")
    print("    FIX: pip install streamlit")
    sys.exit(1)

# ── Done ───────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  ✅ All checks passed! Run the app with:")
print("     streamlit run app.py")
print("=" * 55 + "\n")
