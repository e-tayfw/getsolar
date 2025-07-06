import streamlit as st

st.set_page_config(
    page_title="GetSolar's Personal Testing Interface",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("GetSolar's Personal Interface")

st.sidebar.info("Choose the following functionalities for your needs.")

st.markdown(
    """
    ## Description
    This project introduces a [Streamlit](https://streamlit.io) application designed to interface seamlessly with the [DSPy](https://github.com/stanfordnlp/dspy) framework by StanfordNLP, encapsulated within a [FastAPI](https://github.com/tiangolo/fastapi) backend. 
    It offers an intuitive and interactive frontend solution, showcasing the capabilities of DSPy through a user-friendly web interface. The application leverages [Ollama](https://github.com/ollama/ollama) for small language tasks, [Weaviate Vector DB](https://github.com/weaviate/weaviate) for vector storage, [OpenAI](https://openai.com/) for complex model tasks, and [MLFlow](https://github.com/mlflow/mlflow) for an observability layer.

    In the following application, we have broken down into various chats designed for different functionalities. The application is designed to be user-friendly and interactive, allowing testers to interact with the backend API through the frontend interface.
    In this applications, we have 4 modules which are:
    - Customer Support Chat Bot 
    - Ops Coordination, Chat used to mimic emails and messages from leads

    
"""
)
