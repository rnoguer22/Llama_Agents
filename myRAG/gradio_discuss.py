import urllib.request
import requests
import json
import os



# Función para generar preguntas o discutir sobre archivos
def discutir_archivos(archivos):
    for archivo in archivos:
        if archivo == 'blocks.txt':
            prompt = f"¿Qué es {archivo}?"
            print(f'Prompt: {prompt}')
            respuesta = llama3_predict(prompt)
            return respuesta

# Función para realizar solicitudes al modelo de IA
def llama3_predict(prompt):
    data = {
        "model": "llama3.1",
        "messages": [
            {
            "role": "user",
            "content": prompt
            }
        ],
        "stream": False
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = "http://localhost:11434/api/chat"
    response = requests.post(url, headers=headers, json=data)
    return(response.json()['message']['content'])



if __name__ == '__main__':

    file_path = os.listdir('./myRAG/data/')
    print(discutir_archivos(file_path))