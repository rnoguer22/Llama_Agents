from myRAG.streamlit_app import Llama3_RAG

class Launcher:

    def launch():
        rag = Llama3_RAG()
        rag.set_streamlit_config()
        chain = rag.show_upload_documents()
        rag.show_message_history() 
        rag.show_chat_input(chain)