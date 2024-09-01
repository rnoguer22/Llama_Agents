from time import sleep
import streamlit as st
from myRAG.streamlit_app import Llama3_RAG
from myRAG.scrapper.scrape import scrape_website, split_chunks

class Launcher:

    def __init__(self) -> None:
        self.rag = Llama3_RAG()
        self.rag.set_streamlit_config()


    def launch_main(self, error_id_key: int = 0):
        chain = self.rag.show_upload_documents(error_id_key)
        if chain is not None:
            self.rag.show_message_history() 
            self.rag.show_chat_input(chain)
        else:
            sleep(15)
            error_id_key += 1
            self.launch(error_id_key=error_id_key)


    def launch_web_scrapper(self):
        st.title("Web Scrapper")
        st.text('Provide a valid URL to scrape and to ask questions:')
        url = st.text_input('Enter the website URL to scrape')
        if st.button('Scrape URL'):
            with st.spinner(f'Scrapping {url}...'):
                sleep(1)
                html = scrape_website(url)
                if html:
                    st.session_state.dom_content = html
                    with st.expander('View the URL content'):
                        st.text(html)
                else:
                    st.error(f'Could not scrape the given URL')
                    st.warning('Please reload the page to continue')
    

    def launch(self):
        pg = st.navigation([    
            st.Page(self.launch_main, title="Document reader", icon="🔥"),
            st.Page(self.launch_web_scrapper, title="Web scrapper URL", icon=":material/favorite:"),
            ])
        pg.run()