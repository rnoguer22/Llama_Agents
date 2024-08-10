import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer



model_name = "meta-llama/Meta-Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def generar_resumen(texto):
    # Preproceso del texto (por ejemplo, eliminar tildes, convertir a minúsculas)
    texto = texto.lower()  # Simplificando para este ejemplo
    
    # Tokenización del texto
    inputs = tokenizer.encode_plus(
        texto,
        add_special_tokens=True,
        max_length=512,  # Longitud máxima de la entrada
        return_attention_mask=True,
        return_tensors='pt',
    )
    
    # Preparación de los datos para el modelo (sin necesidad de manipulaciones adicionales)
    outputs = model.generate(inputs['input_ids'])
    
    # Devolución del resumen como string
    texto_salida = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return texto_salida

def leer_archivo(file_path):
    try:
        with open(file_path, 'r') as archivo:
            texto = archivo.read()
            return texto
    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return None


# Ejemplo de uso:
texto_ejemplo = leer_archivo('./meeting_notes/problems.txt')
resumen_generado = generar_resumen(texto_ejemplo)
print('\n'*3, resumen_generado)
