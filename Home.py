# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select
from st_pages import get_nav_from_toml, add_page_title

setting()

# Sidebar
nav = get_nav_from_toml(".streamlit/pages.toml")
pg = st.navigation(nav)
add_page_title(pg)
###########################################################################
# Page 시작
###########################################################################
st.markdown("Hello")

