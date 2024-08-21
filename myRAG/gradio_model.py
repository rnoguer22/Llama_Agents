import os
from dotenv import load_dotenv

from ragbase.config import Config
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate





class Gradio_Model:

    def __init__(self) -> None:
        self.files_dir = './myRAG/data'
        load_dotenv()


    # Funcion para obtener el contenido de los archivos scrapeados de gradio
    def get_files(self):
        files_data = []
        for file in os.listdir(self.files_dir):
            file_path = os.path.join(self.files_dir, file)
            with open(file_path, 'r', encoding='utf-8') as opened_file:
                file_content = opened_file.read()
                files_data.append(file_content)
        return '\n'.join(files_data)
    

    def ask_question(self, file_content):
        llm = ChatGroq(
            temperature=Config.Model.TEMPERATURE,
            model_name=Config.Model.REMOTE_LLM,
            max_tokens=Config.Model.MAX_TOKENS
        )

        prompt = PromptTemplate(
            input_variables=["content", "question"],
            template="Based on the following content:\n\n{content}\n\nAnswer the following question:\n\n{question}\n"
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        question = str(input('Ask your question here: '))
        
        answer = chain.run(content=file_content, question=question)
        
        print("Question:", question)
        print("Answer:", answer)
        print("\n")





gradio_try = Gradio_Model()
file_content = gradio_try.get_files()
gradio_try.ask_question(file_content)