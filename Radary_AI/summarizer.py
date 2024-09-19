from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain

def summarize(feedbacks_list):
    """
        Summarize a list of user feedbacks into a verbose and coherent summary.

        Args:
            feedbacks_list (list): A list of user feedbacks as strings.

        Returns:
            summary (str): A verbose summary of the user feedbacks.
    """
    
    # Join the feedbacks into a single string with bullet points
    feedbacks = "\n*".join(feedbacks_list)
    
    # Create a Document object with the feedbacks
    feedbacks_doc = Document(page_content=feedbacks)
    
    # Define the prompt for the summarization task
    prompt = """
    You will be given a series of user feedbacks , The feedbacks will be enclosed in triple backticks (```)
    Your goal is to give a verbose summary of what said in those feedbacks.
    The finall summary you give me should be coherance and easy to grasp the whole feedbacks.

    ```{text}```
    VERBOSE SUMMARY:
    """
    
    # Create a PromptTemplate object with the prompt and input variable
    prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
    
    # Load the summarization chain with the LLM and prompt template
    chain = load_summarize_chain(
        llm=llm,
        prompt=prompt_template
        )
    
    # Invoke the chain with the feedbacks document and get the output
    output = chain.invoke([feedbacks_doc])
    summary = output['output_text']
    
    return summary


GOOGLE_API_KEY = "AIzaSyDwX1XxrnPMAZhUD0DRgp0K1-EvQeqMZ3Y"
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)