from model import create_chat_groq
import prompt
from langchain_core.exceptions import LangChainException

def generate_code(language,task):
    """ 
    Function to generate code

    Args:
        language (str) - language of the poem
        task (str) - task
    
    Returns:
        Response string ( code )
    """
    try:
        prompt_template = prompt.code_generator_prompt_from_hub()
        llm = create_chat_groq()
        chain = prompt_template | llm
        response = chain.invoke({
            "language" : language,
            "task" : task
        })
        return response.content
    except LangChainException as e:
        return f"Error: {str(e)}"