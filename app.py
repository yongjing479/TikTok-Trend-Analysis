import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import ast

# Configure plotly theme for dark mode
template = pio.templates["plotly_dark"]
template.layout.update(
    paper_bgcolor="rgba(26, 32, 44, 0.0)",
    plot_bgcolor="rgba(26, 32, 44, 0.0)",
    font_color="#e2e8f0"
)
pio.templates.default = template

# Update plotly express defaults
px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = "blues"

# Import section modules
from trend_forecast import show_trend_forecast
from trending_creators import show_trending_creators
from trending_songs import show_trending_songs
from trending_keywords import show_trending_keywords
from trending_hashtags import show_trending_hashtags

# Configure page and theme
st.set_page_config(
    page_title="TikTok Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Custom CSS for tabs
st.markdown('''
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        padding: 0px 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border: none;
        color: #adb5bd;
        font-size: 16px;
        font-weight: 600;
        padding: 0px 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-radius: 0px;
        border-bottom: 3px solid #7f7fd5;
        color: #ffffff;
    }
    </style>''', unsafe_allow_html=True)

# Gradient title using HTML and CSS (purple-blue)
st.markdown(
    '''<h1 style="font-size:3em; font-weight:bold; background: linear-gradient(90deg, #7f7fd5 0%, #86a8e7 50%, #91eac9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TikTok Trends</h1>''',
    unsafe_allow_html=True
)
st.subheader("An interactive dashboard for digital creators")

# Create tabs for navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Trend Forecast",
    "Trending Creators",
    "Trending Songs",
    "Trending Keywords",
    "Trending Hashtags",
    "Trending Challenges",
    "Industry Analysis",
    "Emerging Topics"
])

# Content for each tab
with tab1:
    show_trend_forecast()
with tab2:
    show_trending_creators()
with tab3:
    show_trending_songs()
with tab4:
    show_trending_keywords()
with tab5:
    show_trending_hashtags()
with tab6:
    from trending_challenges import show_trending_challenges
    show_trending_challenges()
with tab7:
    from industry_analytics import show_industry_analytics
    show_industry_analytics()
with tab8:
    from topic_modeling import show_topic_modeling
    show_topic_modeling()

