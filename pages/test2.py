# python -m streamlit run Home.py
import streamlit as st
from core.utils import *
from streamlit_image_select import image_select
from streamlit_tags import st_tags

setting()

# llm 관련
from pathlib import Path 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
#-------------------------------------------------------------------
# Settings
#-------------------------------------------------------------------
key_expander = "isexpanded"
key_chain = "demo_chain"
key_memory = "demo_memory"
key_history = "demo_history"

if "chat_start" not in st.session_state:
    st.session_state["chat_start"] = False

def chat_start():
    st.session_state["chat_start"] = True
    try:
        del st.session_state[key_history]
        del st.session_state[key_memory]
        del st.session_state[key_chain]
    except:
        pass
#-------------------------------------------------------------------
# Header
#-------------------------------------------------------------------
with st.expander(
        label=":gear: Settigns"
    ):  

    # Print Template
    persona = st.text_area(
        label="TEMPLATE",
            value="",
            height=300
    )
    
    # Start Button
    start_btn = st.button(
        label="CHAT START",
        use_container_width=True,
        type="primary",
        on_click=chat_start
    )

if st.session_state["chat_start"]:
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
                ("system", persona),
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
    