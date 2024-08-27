# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select

setting()

###########################################################################
# Functions
###########################################################################
def make_card(col, idx):
    with col:
        with st.container(border=True):
            st.image("https://i.postimg.cc/XJ9gFk48/openart-image-CKz-Cdiz-L-1724052914963-raw.jpg")
            st.markdown("Hello")
            st.button("채팅하기", key=idx, use_container_width=True)
###########################################################################
# Page 시작
###########################################################################
st.session_state["Home"] = "여기는 Home 입니다."
if "create_btn" not in st.session_state:
    st.session_state["create_btn"] = 1

img_url = "https://i.postimg.cc/XJ9gFk48/openart-image-CKz-Cdiz-L-1724052914963-raw.jpg"

st.markdown("Hello")

columns = st.columns(spec=[0.2,0.6,0.2])
with columns[1]:
    img = image_select("캐릭터 생성", [img_url], return_value="index", key="create_btn")
    
if st.session_state["create_btn"] == 0:
    st.switch_page("pages/02_create_character.py")

st.markdown("캐릭터 목록")

columns = st.columns(4, gap="medium")

make_card(columns[0],1)
make_card(columns[1],2)
make_card(columns[2],3)
make_card(columns[3],4)

columns = st.columns(4, gap="medium")

make_card(columns[0],5)
make_card(columns[1],6)
make_card(columns[2],7)
make_card(columns[3],8)
