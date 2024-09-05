from bs4 import BeautifulSoup
import requests
import os



class ScrappedFile:

    def __init__(self, path) -> None:
        self.path = path
        self.name = self.get_name(path)


    # Metodo para darle un nombre al archivo scrapeado de la web
    def get_name(self, path):
        name = path[8:].replace('.', '_')
        name = name.replace('/', '_')
        if name.endswith('_'):
            name = name[:-1]
        return name + '.txt'


    #Metodo para obtener el HTML de la web
    def getvalue(self):
        try:
            # Realizar una solicitud GET para obtener el HTML de la página
            response = requests.get(self.path)
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

            # Quitamos lineas en blanco innecesarias del contenido de la pagina
            cleaned_text = '\n'.join(
                line.strip() for line in visible_text.splitlines() if line.strip()
            )
            return cleaned_text.encode('utf-8')


    # Metodo para separar el contenido de la web en chunks + pequeños
    def split_chunks(dom_content, max_length=8000):
        return [
            dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
        ]