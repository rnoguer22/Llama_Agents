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


'''from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

login(token = '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')

tokenizer = AutoTokenizer.from_pretrained(
"meta-llama/Meta-Llama-3-8B",
cache_dir="/kaggle/working/"
)

model = AutoModelForCausalLM.from_pretrained(
"meta-llama/Meta-Llama-3-8B",
cache_dir="/kaggle/working/",
device_map="auto",
)'''

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



def load_documents(directory):
    #Load the pdf or txt documents from the directory
    loader = DirectoryLoader(directory) #Hay otros muchos loaders en huggingface pero este es el + conveniente
    documents = loader.load()

    #Split the document into chunks --> Los separamos en chunks para que vaya + rapido
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    return docs



@st.cache_resource #Para que la base de datos de chroma corra en cache
def get_chroma_instance():
    #Obtenemos el documento dividido en chunks
    docs = load_documents(rag_directory)

    #create the open-source embedding function --> Para el tema de los vectores de la base de datos y tal
    embedding_function = SentenceTransformerEmbeddings(model_name='all_MiniLM-L6-v2')

    #load it into chroma
    return Chroma.from_documents(docs ,embedding_function)

db = get_chroma_instance()



def query_documents(question):
    """
    Uses RAG to query documents for information to answer a question

    Example call:

    query_documents("What are the action items from the meeting on the 20th?")
    Args:
        question (str): The question the user asked that might be answerable from the searchable documents
    Returns:
        str: The list of texts (and their sources) that matched with the question the closest using RAG
    """
    similar_docs = db.similarity_search(question, k=5)
    docs_formatted = list(map(lambda doc: f"Source: {doc.metadata.get('source', 'NA')}\nContent: {doc.page_content}", similar_docs))

    return docs_formatted  



def prompt_ai(messages):
    # Fetch the relevant documents for the query
    user_prompt = messages[-1].content
    retrieved_context = query_documents(user_prompt)
    formatted_prompt = f"Context for answering the question:\n{retrieved_context}\nQuestion/user input:\n{user_prompt}"    

    # Prompt the AI with the latest user message
    doc_chatbot = ChatHuggingFace(llm=llm)
    ai_response = doc_chatbot.invoke(messages[:-1] + [HumanMessage(content=formatted_prompt)])

    return ai_response



def main():
    st.title("Chat with Local Documents")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=f"You are a personal assistant who answers questions based on the context provided if the provided context can answer the question. You only provide the answer to the question/user input and nothing else. The current date is: {datetime.now().date()}")
        ]    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])        

    # React to user input
    # Example question: What's included in the wellness program Emily proposed?
    # Example question 2: What were the results of the team survey?
    # Example question 3: What was discussed in the meeting on the 22nd?
    if prompt := st.chat_input("What questions do you have?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            ai_response = prompt_ai(st.session_state.messages)
            st.markdown(ai_response.content)
        
        st.session_state.messages.append(ai_response)

if __name__ == 'main':
    main()
