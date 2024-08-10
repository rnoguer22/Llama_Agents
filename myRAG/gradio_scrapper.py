from bs4 import BeautifulSoup
import requests
import os



class Scrap:

    def __init__(self, url):
        self.url = url
    

    def get_urls(self):
        # Realizar una solicitud GET para obtener el HTML de la página
        response = requests.get(self.url)
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Obtener el contenido HTML de la respuesta
            html_content = response.content
            # Crear un objeto BeautifulSoup para analizar el HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            current_link = soup.find('a', class_='thin-link px-4 block leading-8 current-nav-link')
            links = soup.find_all('a', class_='thin-link px-4 block leading-8')
            urls = [current_link.get('href')]
            for link in links:
                urls.append(link.get('href'))
            return urls
        else:
            print('Error al obtener el contenido de la página:', response.status_code)

    

    #Metodo para obtener el HTML de la web
    def get_htmls(self, urls, write:bool=False, save_path:str='./'):
        base_path = 'https://www.gradio.app/docs/gradio/'
        for url in urls:
            web_path = base_path + url
            # Realizar una solicitud GET para obtener el HTML de la página
            response = requests.get(web_path)
            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener el contenido HTML de la respuesta
                html_content = response.content
                # Crear un objeto BeautifulSoup para analizar el HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                # Obtenemos el texto visible de la pagina web
                visible_text = soup.get_text()
                if write:
                    # Imprimir el contenido del cuerpo de la página
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                        print(f'Carpeta {save_path} creada correctamente')
                    file_path = f'{save_path}/{url}.txt'
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(visible_text)
                    print(file_path, ' downloaded successfully')
                else:
                    return visible_text
            else:
                print('Error al obtener el contenido de la página:', response.status_code)


scrapper = Scrap('https://www.gradio.app/docs/gradio/interface')
urls = scrapper.get_urls()
scrapper.get_htmls(urls, write=True, save_path='./myRAG/data/')