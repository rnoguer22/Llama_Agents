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
rag_directory = os.getenv('DIRECTORY', 'meeting_notes')




def main():

if __name__ == 'main':
    main()
