import os
import requests
import uuid

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# 0) Base URL for your FastAPI backend
fastapi_base_url = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")
backend_url = f"{fastapi_base_url}/solar/chat"

# 1) Initialize or retrieve the session’s user_id
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# 2) “Start New Chat” button
if st.sidebar.button("🔄 Start New Chat"):
    st.session_state.user_id  = str(uuid.uuid4())
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me any questions regarding any relevant documents!"}
    ]

# 3) Page config and title
st.set_page_config(page_title="GetSolar Customer Support", page_icon="📝")
st.title("GetSolar AI Chat")

# 4) Initialize chat history if needed
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me any questions regarding any relevant documents!"}
    ]

def get_chat_response(server_url: str, user_id: str, user_query: str):
    payload = {"user_id": user_id, "user_query": user_query}
    res = requests.post(url=server_url, json=payload, timeout=30)
    if res.status_code == 200:
        return res.json()
    st.error(f"Error: {res.status_code} - {res.text}")
    return {"answer": "Sorry, something went wrong."}

# 5) Render the chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6) Input and send
if user_input := st.chat_input("Your question"):
    # record user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # get model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = get_chat_response(
                server_url=backend_url,
                user_id=st.session_state.user_id,
                user_query=user_input
            )
            answer = resp.get("response", "No answer returned.")
            st.write(answer)
            # store assistant message
            st.session_state.messages.append({"role": "assistant", "content": answer})