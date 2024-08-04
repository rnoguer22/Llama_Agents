from langchain_chroma import Chroma
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
import json
import os



load_dotenv()

model = os.getenv('LLM_MODEL', 'meta-llama/Meta-Llama-3.1-8B-Instruct')
#Directory to chat with the local docuements in
rag_directory = os.getenv('DIRECTORY', 'meeting_notes')


@st.cache_resource #We cache it with streamlit so that the modal doesnt instantiate when we rerun the code when the UI reoloads
def get_local_model():
    """return HuggingFaceEndpoint(
        repo_id=model,
        task="text-generation",
        max_new_tokens=1024,
        do_sample=False
    )"""

    #To run the model locally
    return HuggingFacePipeline.from_model_id(
        model_id=model,
        task="text-generation",
        pipeline_kwargs={
            "max_new_tokens": 1024,
            "top_k": 50,
            "temperature": 0.4
        }
    )

llm = get_local_model()



def main():

if __name__ == 'main':
    main()
