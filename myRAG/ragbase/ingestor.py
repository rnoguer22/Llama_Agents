from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFium2Loader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_experimental.text_splitter import SemanticChunker
from langchain_qdrant import Qdrant
from langchain_text_splitters import RecursiveCharacterTextSplitter

from myRAG.ragbase.config import Config


# El objetivo de esta clase es extraer el texto de los PDFs, separarlos en chunks + pequeños
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
            # Obtenemos el texto de los PDFs
            loaded_documents = PyPDFium2Loader(doc_path).load()
            document_text = '\n'.join([doc.page_content for doc in loaded_documents])
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