# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select
from st_pages import show_pages_from_config, add_page_title

setting()

# Sidebar
show_pages_from_config()
add_page_title()
###########################################################################
# Page 시작
###########################################################################
st.markdown("Hello")

