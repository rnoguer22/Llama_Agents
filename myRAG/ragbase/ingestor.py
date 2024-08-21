from pathlib import Path
from typing import List
import streamlit as st

from langchain_community.document_loaders import PyPDFium2Loader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_experimental.text_splitter import SemanticChunker
from langchain_qdrant import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter

from myRAG.ragbase.config import Config


# El objetivo de esta clase es extraer el texto de los archivos, separarlos en chunks + pequeños
# y utilizar un embedding para guardarlos en la vector database
class Ingestor:

    def __init__(self):
        self.embeddings = FastEmbedEmbeddings(model_name=Config.Model.EMBEDDINGS)
        self.semantic_splitter = SemanticChunker(
            self.embeddings, breakpoint_threshold_type='interquartile'
        )
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=128,
            add_start_index=True,
        )


    def ingest(self, doc_paths: List[Path]) -> VectorStore:
        documents = []
        for doc_path in doc_paths:
            doc_path = str(doc_path)

            if doc_path.endswith('.pdf'):
                # Obtenemos el texto de los PDFs
                loaded_documents = PyPDFium2Loader(doc_path, extract_images=True).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])
                    
            elif doc_path.endswith('.txt'):
                # Obtenemos el texto de los txt
                with open(doc_path, 'r') as loaded_document:
                    document_text = loaded_document.read()
            
            elif doc_path.endswith('.csv'):
                loaded_documents = CSVLoader(doc_path).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents]) 

            elif doc_path.endswith('.json'):
                loaded_documents = JSONLoader(doc_path, jq_schema='.', text_content=False).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])

            elif doc_path.endswith('.md'):
                loaded_documents = UnstructuredMarkdownLoader(doc_path).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])

            elif doc_path.endswith('.html'):
                loaded_documents = UnstructuredHTMLLoader(doc_path).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])

            elif doc_path.endswith('docx'):
                loaded_documents = Docx2txtLoader(doc_path).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])
            
            elif doc_path.endswith(('xlsx', 'xls')):
                loaded_documents = UnstructuredExcelLoader(doc_path, mode="elements").load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])
            
            elif doc_path.endswith('pptx'):
                loaded_documents = UnstructuredPowerPointLoader(doc_path).load()
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])

            else:
                # Aqui gestionaremos los archivos que no se puedan leer con langchain para poder intentar leerlos
                pass
            
            if document_text == '\n' or document_text == '':
                    document_name = doc_path.split('/')[-1]
                    document_text = f'No se ha podido cargar el texto del archivo: {document_name}'
                    st.error(document_text, icon='🚨')
                    st.warning('Reload the page to continue')
                    return None 
            
            documents.extend(
                # Dividimos el texto en chunks + pequeños para evitar procesar documentos muy grades
                self.recursive_splitter.split_documents(
                    self.semantic_splitter.create_documents([document_text])
                )
            )
        # Devolvemos una instancia de Qdrant que nos guarda la informacion en vectores
        return Qdrant.from_documents(
            documents=documents,
            embedding=self.embeddings,
            path=Config.Path.DATABASE_DIR,
            collection_name=Config.Database.DOCUMENTS_COLLECTION,
        )