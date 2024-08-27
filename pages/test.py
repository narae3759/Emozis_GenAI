import streamlit as st 
from core.utils import *

setting()

# llm 관련
from pathlib import Path 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter

from google.api_core import exceptions
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
key_expander = "isexpanded"
key_chain = "demo_chain"
key_memory = "demo_memory"
key_history = "demo_history"

def fold_container():
    st.session_state[key_expander] = False

if not key_expander in st.session_state:
    st.session_state[key_expander] = True

if "page" not in st.session_state:
    st.session_state["page"] = 1

def start_chat(data):
    st.session_state["chat_character"] = data
    st.session_state["page"] = 2

def end_chat():
    st.session_state["chat_character"] = None
    del st.session_state[key_history]
    del st.session_state[key_memory]
    del st.session_state[key_chain]
    st.session_state["page"] = 1
#-------------------------------------------------------------------
# Header
#-------------------------------------------------------------------
import requests 
import json 
url = "http://172.16.2.10:8000/character"
response = requests.get(url)
if response.status_code == 200:
    data = {i:x for i, x in enumerate(json.loads(response.text)["data"],1)}
else:
    print("NO")

if st.session_state["page"] == 1:
    # 2행의 열 구성: 각 행에 4개의 열을 생성
    cols = st.columns(4)

    # 각 열에 버튼 추가
    for key, element in data.items():
        # i % 4는 현재 버튼이 어떤 열에 속하는지를 결정합니다 (0부터 3까지의 인덱스)
        col = cols[key % 4]
        
        with col:
            with st.container(border=True):
                st.image(element["profile"])
                st.markdown(element["name"])
                st.button(
                    label="채팅하기", 
                    key=key, 
                    use_container_width=True, 
                    on_click=start_chat,
                    args=[data[key]])


elif st.session_state["page"] == 2:
    st.button("뒤로가기", on_click=end_chat)
    #-------------------------------------------------------------------
    # Sidebar
    #-------------------------------------------------------------------
    with st.sidebar:
        data = st.session_state["chat_character"]
        columns = st.columns(spec=[0.3,0.4,0.3])
        with columns[1]:
            st.image(data["profile"])
        st.markdown(f"이름: {data['name']}")
        st.markdown(f"성격: {data['personality']}")
        st.write(f"상세설명:\n ...")
    #-------------------------------------------------------------------
    # Make Chain
    #-------------------------------------------------------------------
    # 채팅을 이어나갈 때
    if key_chain in st.session_state:
        chain = st.session_state[key_chain]
        memory = st.session_state[key_memory]
        history = st.session_state[key_history]
    # 새로운 템플릿을 적용할 때
    else:
        # 초기화 
        st.session_state[key_history] = []

        # 메모리 설정
        memory = ConversationBufferMemory(
            return_messages=True, 
            memory_key="chat_history"
        )
        # 프롬프트 설정
        # template = read_prompt("./static/templates/Demo.prompt")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", data["details"]),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        # 체인 만들기
        runnable = RunnablePassthrough.assign(
            chat_history = RunnableLambda(memory.load_memory_variables)
            | itemgetter("chat_history")
        )
        model = ChatOpenAI(model_name="gpt-3.5-turbo")
        output_parser = StrOutputParser()
        runnable = RunnablePassthrough.assign(
                chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history")
            )
        chain = runnable | prompt | model | StrOutputParser()
        # 세션 정보 저장
        st.session_state[key_chain] = chain
        st.session_state[key_memory] = memory
    #-------------------------------------------------------------------
    # Chat Messages
    #-------------------------------------------------------------------
    # 첫 채팅을 시작할 때 첫 인사 출력
    if len(st.session_state[key_history]) == 0:
        greeting = "안녕하세요😋"
        st.chat_message("assistant").markdown(greeting)
        st.session_state[key_history].append(
            {"role":"assistant", "content": greeting}
        )
    # 채팅 기록이 있을 때 기록된 채팅 출력
    else:
        for chat in st.session_state[key_history]:
            st.chat_message(chat["role"]).markdown(chat["content"])

    # 채팅창 입력
    question = st.chat_input(placeholder="메세지를 입력하세요")

    if question:
        # 입력된 채팅 출력
        st.chat_message("user").markdown(question)
        st.session_state[key_history].append(
            {"role":"user", "content":question}
        )
        # 답변 출력
        with st.chat_message("assistant"):
            container = st.empty()
            answer = ""
            inputs = {
                "input": question
            }
            # print(chain)
            
            for token in chain.stream(inputs):
                answer += token
                container.markdown(answer)
        
        st.session_state[key_history].append(
            {"role":"assistant", "content":answer}
        )
        # 메모리 저장
        memory.save_context(
            {"inputs": question},
            {"output": answer}
        )

        # 메모리 출력
        # print(memory.load_memory_variables({}))
