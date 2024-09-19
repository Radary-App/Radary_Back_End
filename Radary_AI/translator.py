from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = "AIzaSyDwX1XxrnPMAZhUD0DRgp0K1-EvQeqMZ3Y"
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0, 
    convert_system_message_to_human=True)


def translate(sentence, lang="Arabic"):
    """
    Translate a given sentence from English to the specified language or vice versa.

    Args:
        sentence (str): The sentence to be translated.
        lang (str, optional): The target language for translation. Defaults to "Arabic".

    Returns:
        str: The translated sentence.
    """
    
    system_message = f"You are a helpful assistant that translates English to {lang} vice verca. Translate the user sentence."
    messages = [
        (
            "system",
            system_message,
        ),
        ("human", sentence),
    ]

    translatation = llm.invoke(messages)
    return translatation.content
