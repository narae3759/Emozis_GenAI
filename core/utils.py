import streamlit as st
from pathlib import Path 
from dotenv import load_dotenv 

def setting():
    load_dotenv()
    read_mdfile("./static/css/css.md")

def read_mdfile(filepath:str) -> st.markdown:
    """markdown 파일을 읽고 markdown으로 작성하는 함수

    Args:
        filepath (str): markdown 파일 경로

    Returns:
        str: markdown 파일에서 추출된 텍스트
    """
    file = Path(filepath)
    
    if not file.is_file():
        file_text = f"[ERROR] 파일 경로를 찾을 수 없습니다.(INPUT PATH: {filepath})"
    else:
        file_text = file.read_text(encoding="utf-8")

    return st.markdown(file_text, unsafe_allow_html=True)
