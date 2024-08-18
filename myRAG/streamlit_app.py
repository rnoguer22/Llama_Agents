import asyncio
import random
import streamlit as st
from dotenv import load_dotenv

from myRAG.ragbase.chain import ask_question, create_chain
from myRAG.ragbase.config import Config
from myRAG.ragbase.ingestor import Ingestor
from myRAG.ragbase.model import create_llm
from myRAG.ragbase.retriever import create_retriever
from myRAG.ragbase.uploader import upload_files





class Llama3_RAG:

    def __init__(self) -> None:    
        load_dotenv()
        self.LOADING_MESSAGES = [
            "Winter is coming... Just a moment...",
            "Daenerys is commanding her dragons... Loading...",
            "The Night King is gathering his army... Please wait...",
            "Tyrion is pouring some wine... Hang tight...",
            "The Wall is being rebuilt... One moment...",
            "Bran is warging into a raven... Loading...",
            "The Red Wedding preparations are underway... Please wait...",
            "Cersei is plotting in King's Landing... Hold on...",
            "The Dothraki are preparing for battle... Just a moment...",
            "Sansa is making plans in Winterfell... Loading...",
            "The Hound is sharpening his sword... Please wait...",
            "Melisandre is gazing into the flames... Just a moment...",
            "The Wildlings are crossing the Wall... Loading...",
            "Jaime is riding to the North... Hang tight...",
            "Varys is whispering secrets... Please wait...",
            "The Three-Eyed Raven is seeing the past... Loading...",
            "Dragonglass is being mined... Hold on...",
            "The Great Houses are forming alliances... Just a moment...",
            "The Unsullied are taking their positions... Loading...",
            "Podrick is singing a song... Please wait...",
        ]


    def set_streamlit_config(self):
        st.set_page_config(page_title='RAG Llama 3.1', page_icon='🦙')
        st.html(
            '''
            <style>
                .st-emotion-cache-1eo1tir {
                    width: 70%;
                    max-width: None;
                }

                .st-emotion-cache-p4micv {
                    width: 4rem;
                    height: 4rem;
                }

                .st-emotion-cache-arzcut {
                    width: 70%;
                    max-width: None;
                }
            </style>
            '''
        )
        # Si no hemos escrito nada, damos el mensaje de bienvenida del bot
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    'role': 'assistant',
                    'content': 'What do you want to know about your file?',
                }
            ]

        # Establecemos un limite de mensajes en esta demo, añadiendo nuestras propias advertencias
        if Config.CONVERSATION_MESSAGES_LIMIT > 0 and Config.CONVERSATION_MESSAGES_LIMIT <= len(st.session_state.messages):
            st.warning('You have reached the conversation limit. Refresh the page to start a new conversation.')
            st.stop()


    # Esta funcion es la que lo hace casi todo xddd
    @st.cache_resource(show_spinner=True)
    def build_qa_chain(_self, files):
        file_paths = upload_files(files)
        vector_store = Ingestor().ingest(file_paths)
        if vector_store is not None:
            llm = create_llm()
            retriever = create_retriever(llm, vector_store=vector_store)
            return create_chain(llm, retriever)
        return None


    # La respuesta va a ser un async generator, por lo que usamos una funcion asincrona
    async def ask_chain(self, question: str, chain):
        full_response = ''
        assistant = st.chat_message(
            'assistant', avatar=str(Config.Path.IMAGES_DIR / 'assistant-avatar.png')
        )
        with assistant:
            # Definimos un placeholder vacio para que se muestre un texto cuando la aplicacion esta en ejecucion
            message_placeholder = st.empty()
            message_placeholder.status(random.choice(self.LOADING_MESSAGES), state='running')
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
    def show_upload_documents(self, generated_key: int = 0):
        holder = st.empty()
        with holder.container():
            st.header('RagBase')
            st.subheader('Get answers from your documents')
            uploaded_files = st.file_uploader(
                label='Upload the file(s) data', type=['pdf', 'txt'], accept_multiple_files=True, key=generated_key
            )

        if not uploaded_files:
            st.warning('Please upload PDF or .txt document to continue!')
            st.stop()
        
        with st.spinner('Analyzing your document(s)...'):
            holder.empty()
            return self.build_qa_chain(files=uploaded_files)


    # Funcion para mostrar el historial de mensajes
    def show_message_history(self):
        for message in st.session_state.messages:
            role = message['role']
            avatar_path = (
                Config.Path.IMAGES_DIR / 'assistant-avatar.png'
                if role == 'assistant'
                else Config.Path.IMAGES_DIR / 'user-avatar.png'
            )
            with st.chat_message(role, avatar=str(avatar_path)):
                st.markdown(message['content'])


    def show_chat_input(self, chain):
        if prompt := st.chat_input('Ask your question here!'):
            st.session_state.messages.append({'role': 'user', 'content': prompt})
            with st.chat_message(
                'user',
                avatar=str(Config.Path.IMAGES_DIR / 'user-avatar.png'),
            ):
                st.markdown(prompt)
            asyncio.run(self.ask_chain(prompt, chain))