from bs4 import BeautifulSoup
import requests
import os
import streamlit as st




#Metodo para obtener el HTML de la web
def scrape_website(url, write: bool = False, save_path: str = './'):
    try:
        # Realizar una solicitud GET para obtener el HTML de la página
        response = requests.get(url)
    except: 
        return None

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el contenido HTML de la respuesta
        html_content = response.content
        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Obtenemos el texto visible de la pagina web
        visible_text = soup.get_text(separator='\n')

        if write:
            # Imprimir el contenido del cuerpo de la página
            if not os.path.exists(save_path):
                os.makedirs(save_path)
                print(f'Carpeta {save_path} creada correctamente')
            file_path = f'{save_path}/{url}.txt'
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(visible_text)
            print(file_path, ' downloaded successfully')

        # Quitamos lineas en blanco innecesarias del contenido de la pagina
        cleaned_text = '\n'.join(
            line.strip() for line in visible_text.splitlines() if line.strip()
        )
        return cleaned_text


# Metodo para separar el contenido de la web en chunks + pequeños
def split_chunks(dom_content, max_length=8000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]