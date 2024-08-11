import asyncio
import random
import streamlit as st
from dotenv import load_dotenv

from ragbase.chain import ask_question, create_chain
from ragbase.config import Config
from ragbase.ingestor import Ingestor
from ragbase.model import create_llm
from ragbase.retriever import create_retriever
from ragbase.uploader import upload_files



load_dotenv()

st.set_page_config(page_title='RAG Llama 3.1', page_icon='🦙')

LOADING_MESSAGES = [
    # The Lord of the Rings
    "Gollum is searching for his 'precious'... Please wait...",
    "Gandalf is reading the ancient texts... One moment...",
    "Frodo is one step closer to Mordor... Please wait...",

    # Game of Thrones
    "John Snow is riding Rhaegal... One moment...",
    "The Iron Throne is being forged... Please wait...",
    "Arya is changing her face... Loading...",

    # The Hobbit
    "Smaug is guarding his treasure... One moment...",
    "Bilbo is negotiating with the trolls... Please wait...",
    "Gandalf is preparing his pipe... Loading...",
    "The dwarves are preparing the siege on Erebor... Loading...",
    "The path to the Lonely Mountain is clearing... One moment...",

    # Harry Potter
    "The train to Hogwarts is on its way... Please wait...",
    "The spells are being prepared... Loading...",
    "Hermione is searching through her library... One moment...",
    "Dobby is bringing the butterbeer... Loading...",
    "The Sorting Hat is deciding... One moment...",

    # Star Wars
    "The Force is awakening... Loading...",
    "The Millennium Falcon is calculating the escape route... Please wait...",
    "Yoda is meditating on Dagobah... One moment...",
    "Luke is tuning his lightsaber... Loading...",
    "The Empire is building a new Death Star... Please wait..."
]




# Esta funcion es la que lo hace casi todo xddd
@st.cache_resource(show_spinner=True)
def build_qa_chain(files):
    file_paths = upload_files(files)
    vector_store = Ingestor().ingest(file_paths)
    llm = create_llm()
    retriever = create_retriever(llm, vector_store=vector_store)
    return create_chain(llm, retriever)


# La respuesta va a ser un async generator, por lo que usamos una funcion asincrona
async def ask_chain(question: str, chain):
    full_response = ''
    assistant = st.chat_message(
        'assistant', avatar=str(Config.Path.IMAGES_DIR / 'assistant-avatar.png')
    )
    with assistant:
        # Definimos un placeholder vacio para que se muestre un texto cuando la aplicacion esta en ejecucion
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state='running')
        documents = []
        async for event in ask_question(chain, question, session_id='session-id-42'):
            if type(event) is str:
                full_response += event
                message_placeholder.markdown(full_response)
            if type(event) is list:
                documents.extend(event)
        for i, doc in enumerate(documents):
            # Añadimos un expander para ver de donde obtiene la informacion el asistente
            with st.expander(f'Source *{i+1}'):
                st.write(doc.page_content)
    # Añadimos la respuesta al session_state para quu el chat_history funcione correctamente
    st.session_state.messages.append({'role': 'assistant', 'content': full_response})


# Funcion para subir los archivos
def show_upload_documents():
    holder = st.empty()
    with holder.container():
        st.header('RagBase')
        st.subheader('Get answers from your documents')
        uploaded_files = st.file_uploader(
            label='Upload the PDF data', type=['pdf'], accept_multiple_files=True
        )
    if not uploaded_files:
        st.warning('Please upload PDF documents to continue!')
        st.stop()
    
    with st.spinner('Analyzing your document(s)...'):
        holder.empty()
        return build_qa_chain(uploaded_files)


# Funcion para mostrar el historial de mensajes
def show_message_history():
    for message in st.session_state.meesages:
        role = message['role']
        avatar_path = (
            Config.Path.IMAGES_DIR / 'assistant-avatar.png'
            if role == 'assistant'
            else Config.Path.IMAGES_DIR / 'user-avatar.png'
        )
        with st.chat_message(role, avatar=str(avatar_path)):
            st.markdown(message['content'])


def show_chat_input(chain):
    if prompt := st.chat_input('Ask your question here!'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message(
            'user',
            avatar=str(Config.Path.IMAGES_DIR / 'user-avatar.png'),
        ):
            st.markdown(prompt)
        asyncio.run(ask_chain(prompt, chain))



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