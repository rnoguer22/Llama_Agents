import os
from dotenv import load_dotenv



class Gradio_Model:

    def __init__(self) -> None:
        self.files_dir = './myRAG/data'
        load_dotenv()


    # Funcion para obtener el contenido de los archivos scrapeados de gradio
    def get_files(self):
        files_data = []
        for file_name in os.listdir(self.files_dir):
            uploaded_file = UploadedGradioFile(file_name)
            files_data.append(uploaded_file)
        return files_data
    


class UploadedGradioFile(Gradio_Model):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


    def getvalue(self):
        file_path = os.path.join(self.files_dir, self.name)
        with open(file_path, 'rb') as opened_file:
            file_content = opened_file.read()
        return file_content