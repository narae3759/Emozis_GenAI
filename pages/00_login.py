# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select

setting()

###########################################################################
# Functions
###########################################################################

url = "http://localhost:8000/character"

columns = st.columns(spec=[0.2,0.6,0.2])
with columns[1]:
    with st.form(key="login"):
        st.markdown("SIGN IN")
        nickname = st.text_input(label="ID")
        password = st.text_input(label="PW")

        login_btn = st.form_submit_button(label="Sign In", use_container_width=True, type="primary")

