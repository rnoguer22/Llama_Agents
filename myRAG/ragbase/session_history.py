from langchain_community.chat_message_histories import ChatMessageHistory


store = {}

# Funcion para crear un nuevo historial de mensajes al iniciar la aplicacion
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
