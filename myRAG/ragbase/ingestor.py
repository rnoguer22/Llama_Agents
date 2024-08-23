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
from langchain_community.document_loaders.image import UnstructuredImageLoader

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
        #Funcion para mostrar mensajes de error
        def show_error(message_error):
            st.error(message_error, icon='🚨')
            st.warning('Reload the page to continue')
            return None

        documents = []
        for doc_path in doc_paths:
            doc_path = str(doc_path)
            document_name = doc_path.split('/')[-1]
            if doc_path.endswith('.pdf'):
                # Obtenemos el texto de los PDFs
                loaded_documents = PyPDFium2Loader(doc_path, extract_images=True).load()
            elif doc_path.endswith('.csv'):
                loaded_documents = CSVLoader(doc_path).load()
            elif doc_path.endswith('.json'):
                loaded_documents = JSONLoader(doc_path, jq_schema='.', text_content=False).load()
            elif doc_path.endswith('.md'):
                loaded_documents = UnstructuredMarkdownLoader(doc_path).load()
            elif doc_path.endswith('.html'):
                loaded_documents = UnstructuredHTMLLoader(doc_path).load()
            elif doc_path.endswith('docx'):
                loaded_documents = Docx2txtLoader(doc_path).load()
            elif doc_path.endswith(('xlsx', 'xls')):
                loaded_documents = UnstructuredExcelLoader(doc_path, mode="elements").load()
            elif doc_path.endswith('pptx'):
                loaded_documents = UnstructuredPowerPointLoader(doc_path).load()
            elif doc_path.endswith((".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg", ".heif", ".heic", ".psd", ".ico", ".eps")):
                return show_error(f'No se ha podido cargar el texto del archivo {document_name}; No se permiten imagénes!!!')
            else:
                # Las demas extensiones de archivos, las intentamos leer sin langchain (archivos de python, java, etc.)
                try:
                    with open(doc_path, 'r') as loaded_document:
                        document_text = loaded_document.read()
                except:
                    # Si obtenemos error, es que no podemos leer el archivo
                    return show_error(f'El archivo {document_name} contiene una extension no soportada.')
            
            try:
                # Obtenemos el texto de los archivos subidos por el usuario
                document_text = '\n'.join([doc.page_content for doc in loaded_documents])
            except:
                pass
            
            if document_text == '\n' or document_text == '':
                    return show_error(f'No se ha podido cargar el texto del archivo {document_name}')

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