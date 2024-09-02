import streamlit as st
from sLLM.search_test import searchtest
import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Test ChatBot', page_icon="🙋")
st.title("🙋 Test Q&A ChatBot")

if user_input:= st.chat_input("메세지를 입력해 주세요"):
    st.chat_message("user").write(f"{user_input}")
    # st.chat_message("assistant").write(f"{'그래 너의 말을 이해했다.'}")
    result = searchtest(user_input)
    st.chat_message("assistant").write(f"{result}")

# sidebar
st.sidebar.image('./data/chatbot.png', caption="TEMP")
with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("Say something"):
        messages.chat_message("user").write(prompt)
        messages.chat_message("assistant").write(f"Echo: {prompt}")

#switcher
st.sidebar.header("")

