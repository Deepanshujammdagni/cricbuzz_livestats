"""
Handles all MySQL database connections for Cricbuzz LiveStats project.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st

# Force load .env from project root - important on Windows where cwd can vary
_dotenv_path = find_dotenv(usecwd=True)
load_dotenv(_dotenv_path, override=True)


def _get_db_config():
    """Reads DB config from environment."""
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),   # 127.0.0.1 more reliable than localhost on Windows
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "cricbuzz_db"),
        "autocommit": True,
        "connection_timeout": 10,
        "use_pure": True,   # avoids C-extension issues on some Windows setups
    }


def get_connection():
    """
    Returns a MySQL connection using environment variables.
    Shows detailed diagnostics to help debug connection issues.
    """
    config = _get_db_config()
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        errno = e.errno if hasattr(e, "errno") else 0

        if errno == 2003:
            st.error(
                f"❌ **Can't connect to MySQL server** on `{config['host']}:{config['port']}`\n\n"
                "**Fix checklist:**\n"
                "1. Open **Services** → Win+R → type `services.msc` → find **MySQL80** → click Start\n"
                "2. Or run in CMD (as Admin): `net start MySQL80`\n"
                "3. Check your `.env` file: `DB_HOST=127.0.0.1` and `DB_PORT=3306`"
            )
        elif errno == 1045:
            st.error(
                f"❌ **Access denied** for user `{config['user']}`\n\n"
                "**Fix:** Check `DB_USER` and `DB_PASSWORD` in your `.env` file."
            )
        elif errno == 1049:
            st.error(
                f"❌ **Unknown database** `{config['database']}`\n\n"
                "**Fix:** Run this in CMD: `mysql -u root -p < schema.sql`"
            )
        else:
            st.error(f"❌ Database error ({errno}): {e}")

        st.info(
            f"🔧 **Config being used** (edit `.env` to fix):\n"
            f"- Host: `{config['host']}`\n"
            f"- Port: `{config['port']}`\n"
            f"- User: `{config['user']}`\n"
            f"- Password: `{'*' * len(config['password']) if config['password'] else '(empty — check DB_PASSWORD)'}`\n"
            f"- Database: `{config['database']}`"
        )
        return None


def run_query(query, params=None, fetch=True):
    """
    Runs a SQL query and returns results as a list of dicts.
    If fetch=False, executes without returning rows (INSERT/UPDATE/DELETE).
    """
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        else:
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            return affected
    except Error as e:
        st.error(f"❌ Query failed: {e}\n\nQuery: `{query[:200]}`")
        return None


def test_connection():
    """
    Silent connection test used by sidebar - returns True/False without showing errors.
    """
    config = _get_db_config()
    try:
        conn = mysql.connector.connect(**config)
        conn.close()
        return True
    except Error:
        return False
