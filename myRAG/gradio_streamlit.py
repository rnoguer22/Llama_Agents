import asyncio
import random
import streamlit as st
from dotenv import load_dotenv



load_dotenv()

st.set_page_config(page_title='RAG Llama 3.1', page_icon='🦙')

# Si no hemos escrito nada, damos el mensaje de bienvenida del bot
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'assistant',
            'content': 'Hi! What do you want to know about Gradio?',
        }
    ]

# Establecemos un limite de mensajes en esta demo, añadiendo nuestras propias advertencias
if Config.CONVERSATION_MESSAGES_LIMIT > 0 and Config.CONVERSATION_MESSAGES_LIMIT <= len(st.session_state.messages):
    st.warning('YOu have reached the conversation limit. Refresh the page to start a new conversation.')
    st.stop()



chain = show_upload_documents()
show_message_history() 
show_chat_input(chain)