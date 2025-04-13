import streamlit as st
import json
import datetime
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

#st.components.v1.html('<meta http-equiv="refresh" content="300">', height=0)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

dark_theme = """
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
        font-size: 1.5rem;
    }
    
    .high-severity {
        border-left: 5px solid #FF4B4B;
    }
    
    .critical-severity {
        border-left: 5px solid #FF0000;
        background-color: #2E1E2E;
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
"""
st.markdown(dark_theme, unsafe_allow_html=True)

st.write(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#Load news data from JSON file
def load_news_data():
    news_file = "newsData.json"
    
    if os.path.exists(news_file):
        try:
            with open(news_file, "r") as f:
                return json.load(f)
        except:
            return []
    else:
        return []

#Load CVE data from JSON file
def load_cve_data():
    cve_file = "cveData.json"
    
    if os.path.exists(cve_file):
        try:
            with open(cve_file, "r") as f:
                return json.load(f)
        except:
            return []
    else:
        return []

# Create two columns
col1, col2 = st.columns(2)

# News column
with col1:
    news_data = load_news_data()
    
    if not news_data:
        st.info("No news data available yet. Wait for the next update.")
    
    for item in reversed(news_data):
        with st.container():
            st.markdown(f"""
            <div class="news-item">
                <h3>{item.get('title', 'No Title')}</h3>
                <p>{item.get('description', 'No description available.')}</p>
                <p class="timestamp">Source: <a href="{item.get('link', '#')}">"{item.get('link', '#')}"</a></p>
            </div>
            """, unsafe_allow_html=True)

# CVE column
with col2:
    cve_data = load_cve_data()
    
    if not cve_data:
        st.info("No CVE data available yet. Wait for the next update.")
    
    for item in reversed(cve_data):
        # Extract severity from title
        title = item.get('title', '')
        
        if "[CRITICAL]" in title:
            severity_class = "critical-severity"
        elif "[HIGH]" in title:
            severity_class = "high-severity"
            
        # Extract CVE ID from title
        cve_id = title.split(" - ")[0] if " - " in title else title
            
        with st.container():
            st.markdown(f"""
            <div class="cve-item {severity_class}">
                <h3>{cve_id}</h3>
                <p><strong>{title.split(" - ")[1] if " - " in title else ""}</strong></p>
                <p>{item.get('description', 'No description available.')}</p>
            </div>
            """, unsafe_allow_html=True)


st.markdown("<div style='margin-bottom:200px;'></div>", unsafe_allow_html=True)

st_autorefresh(interval=2000, limit=None)