from langchain_community.chat_models import ChatOllama
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_groq import ChatGroq

from myRAG.ragbase.config import Config

'''
Archivo para inicializar todos los modelos que vamos a necesitar
'''

# Funcion para crear el llm en local o con la api de groq, segun especifiquemos en config.py
def create_llm() -> BaseLanguageModel:
    #if not groq_api_key:
    if Config.Model.USE_LOCAL:
        return ChatOllama(
            model=Config.Model.LOCAL_LLM,
            temperature=Config.Model.TEMPERATURE,
            keep_alive='1h',
            max_tokens=Config.Model.MAX_TOKENS
        )
    else:
        return ChatGroq(
            temperature=Config.Model.TEMPERATURE,
            model_name=Config.Model.REMOTE_LLM,
            max_tokens=Config.Model.MAX_TOKENS
            #api_key=groq_api_key
        )


def create_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=Config.Model.EMBEDDINGS)


def create_reranker() -> FlashrankRerank:
    return FlashrankRerank(model=Config.Model.RERANKER)