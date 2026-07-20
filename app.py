"""DisasterShield AI — Navigation Entry Point"""
import streamlit as st
from backend.services import push_service

# Background daemon: re-checks disaster risk every 5 min and Web-Pushes
# High/Critical alerts to registered devices even when their browser is closed.
push_service.ensure_daemon()

st.set_page_config(
    page_title="DisasterShield AI",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pg = st.navigation([
    st.Page("frontend/pages/home.py",      title="Dashboard",     url_path="",          default=True),
    st.Page("frontend/pages/risk.py",      title="Risk Monitor",  url_path="risk"),
    st.Page("frontend/pages/assistant.py", title="AI Assistant",  url_path="assistant"),
    st.Page("frontend/pages/resources.py", title="Resources",     url_path="resources"),
    st.Page("frontend/pages/emergency.py", title="Emergency",     url_path="emergency"),
    st.Page("frontend/pages/analytics.py", title="Analytics",     url_path="analytics"),
    st.Page("frontend/pages/settings.py",  title="Settings",      url_path="settings"),
    st.Page("frontend/pages/profile.py",   title="My Profile",    url_path="profile"),
    st.Page("frontend/pages/guide.py",     title="Offline Guide", url_path="guide"),
], position="hidden")

pg.run()
