import streamlit as st
from launcher import Launcher

if __name__ == '__main__':

    def main_page():
        launcher = Launcher()
        launcher.launch()

    def page2():
        st.title("Second page")

    pg = st.navigation([
        st.Page(main_page, title="Document reader", icon="🔥"),
        st.Page(page2, title="Gradio page", icon=":material/favorite:"),
        ])
    
    pg.run()