# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select
from streamlit_tags import st_tags

setting()

###########################################################################
# Functions
###########################################################################
img_url = "https://i.postimg.cc/XJ9gFk48/openart-image-CKz-Cdiz-L-1724052914963-raw.jpg"

st.markdown("Hello")

import streamlit as st

with st.popover("프로필 선택", use_container_width=True):
    image_select("캐릭터 생성", [img_url,img_url,img_url,img_url,img_url,img_url],key=1)

col1, col2 = st.columns(spec=[0.3,0.7])
col1.image(img_url, width=200)
with col2:
    st.text_input(label="Name")
    st.radio(label="Gender", options=["남","여"], horizontal=True)

keywords = st_tags(
    label="Relationship",
    text='관계를 입력하세요',
    value=['웬수', '시어머니'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key=2)

keywords = st_tags(
    label="Personality",
    text='관계를 입력하세요',
    value=['괴팍함', '성격급함'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key=3)

st.text_area(label="Details",height=200)

st.button("캐릭터 생성하기", use_container_width=True, type="primary")