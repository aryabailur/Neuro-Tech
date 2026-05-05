import streamlit as st
from synthesizer import synthesize



st.set_page_config(
    page_title="Neuro-Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a BCI Research Agent by Arya Bailur"
    }
)
st.title("Neuro-Agent: BCI Research Assistant",anchor="main_header", help="This agent fetches ArXiv papers")

if "message" not in st.session_state:
    st.session_state["message"]=[]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]



for message in st.session_state.message:
     with st.chat_message(message["role"]):
         st.write(message["content"])
            

if query:=st.chat_input("What do you want to research about?"):
    st.session_state["message"].append({"role":"user","content":query})
    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Researching..."):
        result=synthesize(query,chat_history=st.session_state["chat_history"])

    st.session_state["chat_history"].append({
    "query": query,
    "response": result
    })

    
    st.session_state["message"].append({"role":"assistant","content":result})
    with st.chat_message("assistant"):
        st.write(result)

with st.sidebar:
    st.title("Neuro-Agent Controls")
    st.markdown("Adjust your research settings below.")