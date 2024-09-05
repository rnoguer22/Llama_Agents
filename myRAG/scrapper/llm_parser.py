from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate



def parse_with_ollama(dom_chunks, parse_description):
    
    template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "If the answer is not found within the text content, state that the answer cannot be found."
    "Prioritize concise responses (maximum of 3 sentences) and use a list where applicable."
    "Use markdown formatting where appropiate."
    )

    model = OllamaLLM(model="llama3.1")

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)