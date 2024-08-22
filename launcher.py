from time import sleep
import streamlit as st
from myRAG.streamlit_app import Llama3_RAG

class Launcher:

    def __init__(self) -> None:
        self.rag = Llama3_RAG()
        self.rag.set_streamlit_config()


    def launch_main(self, error_id_key: int = 0, launch_gradio_docs: bool = False):
        chain = self.rag.show_upload_documents(error_id_key, launch_gradio_docs=launch_gradio_docs)
        if chain is not None:
            self.rag.show_message_history() 
            self.rag.show_chat_input(chain)
        else:
            sleep(15)
            error_id_key += 1
            self.launch(error_id_key=error_id_key)


    def launch_gradio(self):
        st.title("Second page")
    

    def launch(self):
        pg = st.navigation([    
            st.Page(self.launch_main, title="Document reader", icon="🔥"),
            st.Page(self.launch_main(launch_gradio_docs=True), title="Gradio page", icon=":material/favorite:"),
            ])
        pg.run()