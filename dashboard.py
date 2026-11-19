import datetime
import html
import json
import logging
import threading
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit_autorefresh import st_autorefresh

import cveFeed
import newsFunc

BASE_DIR = Path(__file__).parent  # same folder the feed scripts write to, regardless of where streamlit was launched
NEWS_FILE = BASE_DIR / "newsData.json"
CVE_FILE = BASE_DIR / "cveData.json"

UPDATE_INTERVAL_S = 3600   # how often the background thread fetches new data
REFRESH_INTERVAL_MS = 300_000  # how often the page re-reads the JSON files
DISPLAY_ITEMS = 20

log = logging.getLogger(__name__)

#Background update

def update():
    while True:
        for job in (cveFeed.run, newsFunc.run):
            try:
                job()
            except Exception as e:
                print(f"{job.__module__}.run failed: {e}")
        time.sleep(3600)

@st.cache_resource
def start_updater():
    t = threading.Thread(target=update, daemon=True)
    t.start()
    return t

start_updater()

# Page setup
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    :root {
        --background-color: #0E1117;
        --text-color: #FAFAFA;
    }

    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    p, span, div, h1, h2, h3, h4, h5, h6, li {
        color: var(--text-color) !important;
    }

    .stTextInput, .stSelectbox, .stMultiselect {
        background-color: #262730;
    }

    .stButton>button {
        background-color: #4DA8DA;
        color: white;
    }

    .news-item {
        background-color: #1E1E2E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #4DA8DA;
        font-size: 1.5rem;
    }

    .cve-item {
        background-color: #1E1E2E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #FF4B4B;
        font-size: 1.5rem;
    }

    .timestamp {
        color: #888888;
        font-size: 0.8em;
    }

    h1, h2, h3 {
        color: #4DA8DA;
    }

    a {
        color: #4DA8DA;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    .stApp {
        background-color: var(--background-color);
    }
</style>
""", unsafe_allow_html=True)

# Data
def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def last_data_update():
    times = [p.stat().st_mtime for p in (NEWS_FILE, CVE_FILE) if p.exists()]
    if not times:
        return "no data yet"
    tz = ZoneInfo(st.context.timezone or "UTC")
    return datetime.datetime.fromtimestamp(max(times), tz).strftime("%Y-%m-%d %H:%M:%S")

tz = ZoneInfo(st.context.timezone or "UTC")
st.write(f"Last updated: {datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}")

col1, col2 = st.columns(2)

# News column
with col1:
    news_data = load_json(NEWS_FILE)[-DISPLAY_ITEMS:]

    if not news_data:
        st.info("No news data available yet. Wait for the next update.")

    for item in reversed(news_data):
        title = html.escape(item.get("title") or "No Title")
        description = html.escape(item.get("description") or "No description available.")
        link = html.escape(item.get("link") or "#", quote=True)

        st.markdown(f"""
            <div class="news-item">
            <h3>{title}</h3>
            <p>{description}</p>
            <p class="timestamp">Source: <a href="{link}" target="_blank">{link}</a></p>
            </div>
            """, unsafe_allow_html=True)

# CVE column
with col2:
    cve_data = load_json(CVE_FILE)[-DISPLAY_ITEMS:]

    if not cve_data:
        st.info("No CVE data available yet. Wait for the next update.")

    for item in reversed(cve_data):
        title = html.escape(item.get("title") or "No Title")
        description = html.escape(item.get("description") or "No description available.")
        cve_id = html.escape(item.get("id") or "")

        st.markdown(f"""
            <div class="cve-item">
            <h3>{title}</h3>
            <p>{description}</p>
            <p class="cve-id">{cve_id}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:200px;'></div>", unsafe_allow_html=True)

st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None)