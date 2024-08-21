import os





class Gradio_Model:

    def __init__(self) -> None:
        self.files_dir = './myRAG/data'


    def get_files(self):
        files_data = []
        for file in os.listdir(self.files_dir):
            file_path = os.path.join(self.files_dir, file)
            with open(file_path, 'r', encoding='utf-8') as opened_file:
                file_content = opened_file.read()
                files_data.append(file_content)
        return files_data
    


gradio_try = Gradio_Model()
print(gradio_try.get_files())