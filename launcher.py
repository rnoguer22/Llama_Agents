from time import sleep
from myRAG.streamlit_app import Llama3_RAG

class Launcher:

    def __init__(self) -> None:
        self.rag = Llama3_RAG()
        self.rag.set_streamlit_config()

    def launch(self, error_id_key: int = 0):
        chain = self.rag.show_upload_documents(error_id_key)
        if chain is not None:
            self.rag.show_message_history() 
            self.rag.show_chat_input(chain)
        else:
            sleep(15)
            error_id_key += 1
            self.launch(error_id_key=error_id_key)