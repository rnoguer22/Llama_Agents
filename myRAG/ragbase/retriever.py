from typing import Optional

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.chain_filter import LLMChainFilter
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_qdrant import Qdrant

from myRAG.ragbase.config import Config
from myRAG.ragbase.model import create_embeddings, create_reranker



def create_retriever(
    llm: BaseLanguageModel, vector_store: Optional[VectorStore] = None      
) -> VectorStoreRetriever:
    # Si no pasamos la base de datos en la funcion, la creamos con la configuracion del Config
    if not vector_store:
        vector_store = Qdrant.from_existing_collection(
            embedding=create_embeddings,
            collection_name=Config.Database.DOCUMENTS_COLLECTION,
            path=Config.Path.DATABASE_DIR
        )
    # Creamos el retriever con busqueda por similaridad y se va a quedar con los 5 chunks o documentos + relevantes
    retriever = vector_store.as_retriever(
        search_type='similarity', search_kwargs={'k': 5}
    )
    # Si tenemos un reranker lo asignamos al retriever
    if Config.Retriever.USE_RERANKER:
        retriever = ContextualCompressionRetriever(
            base_compressor=create_reranker(), base_retriever=retriever
        )
    # Si tenemos un chain filter, tambien se lo asignamos
    if Config.Retriever.USE_CHAIN_FILTER:
        retriever = ContextualCompressionRetriever(
            base_compressor=LLMChainFilter.from_llm(llm), base_retriever=retriever
        )
    return retriever