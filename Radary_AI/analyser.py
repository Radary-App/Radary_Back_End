from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from pydantic import BaseModel, Field

GOOGLE_API_KEY = "AIzaSyDwX1XxrnPMAZhUD0DRgp0K1-EvQeqMZ3Y"
# initialize llm with ingnoring dangerous content as the imgae will include accidents and fires 
llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            timeout = None,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )

# a class to parse llm output for accident feature to the desired outputs
class accident_analysis(BaseModel):
    description: str = Field(description="description of the photo")
    title: str = Field(description="concise title for the accident (2-4 words)")
    authority: str = Field(description="the most relevent authority that can help in this accident or fire")
    level: int = Field(description="danger level from 1 to 100")

# a class to parse llm output for eco-isseu feature to the desired outputs
class issue_analysis(BaseModel):
    description: str = Field(description="description of the photo")
    title: str = Field(description="concise title for the issue (2-4 words)")
    authority: str = Field(description="authority that can resolve the issue")
    priority: int = Field(description="priority level")




# Wrapper for all analyser to be used in the main.py
class analyser:

    def analyse_accident(image_data_b64):
        """
            Analyze an image that may depict an accident, fire, or other hazardous situation.

            Args:
                image (UploadFile): An image file object uploaded by user.
                language (str, optional): The language in which the response should be provided. Defaults to "En" (English).

            Returns:
                tuple: A tuple containing three pieces of information:
                    - description (str): A thorough description of the photo, including any relevant details.
                    - authority (str): The most relevant authority to contact in order to resolve the issue.
                    - level (int): A danger level from 1 to 100, with 1 being minimal risk and 100 being extreme risk.
        """
        
        # Define the prompt for the image analysis, including the format instructions
        accident_prompt = """
        Analyze the following photo, which may depict an accident, fire, or other hazardous situation.
        Please provide a concise response with the following three pieces of information:
        - Detailed Description:
        Provide a thorough description of the photo, including any relevant details that would be useful for the relevant authority to know.
        - Title:
        Give a concise title for the accident 2-4 words.
        - Recommended Authority:
        Suggest the most relevant authority to contact in order to resolve the issue, such as Police, Hospital, Fire Station, or other emergency services.
        - Danger Level:
        Assign a danger level from 1 to 100, with 1 being minimal risk and 100 being extreme risk, to help prioritize the response to this situation based on its potential danger to people."
        If the photo does not seems to be danger at all (just a normal photo) set the Danger level to 10 
        {format_instructions}
        """
        accident_parser = PydanticOutputParser(pydantic_object=accident_analysis)
        # Create a HumanMessage object with the prompt and image
        accident_message = HumanMessage(
            content=[
                {"type": "text", "text": accident_prompt.format(format_instructions=accident_parser.get_format_instructions())},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_data_b64}"},
                },
            ],
        )

        # Invoke the LLM with the message and get the response
        response = llm.invoke([accident_message])
        
        # Parse the response and extract the description, authority, and danger level
        x = accident_parser.parse(response.content)
        return x.description, x.title, x.authority, x.level


    def analyse_isuue(image_data_b64):
        """
            Analyze an image that may depict environmental issues such as pollution, broken streetlights, and garbage collection.

            Args:
                image (UploadFile): An image file object uploaded by user.
                language (str, optional): The language in which the response should be provided. Defaults to "En" (English).

            Returns:
                tuple: A tuple containing three pieces of information:
                    - description (str): A thorough description of the photo, including any relevant details.
                    - authority (str): The most relevant authority to contact in order to resolve the issue.
                    - priority (int): A priority level from 1 to 5, with 1 being maximum priority and 5 being minimum priority.
        """

        # Define the prompt for the image analysis, including the format instructions
        issue_prompt = """
        Analyze the following photo, which may depict environmental issues such as pollution, broken streetlights, and garbage collection.
        Please provide a concise response with the following three pieces of information:
        - Detailed Description:
        Provide a thorough description of the photo, including any relevant details that would be useful for the relevant authority to know.
        - Title:
        Give a concise title for the accident 2-4 words.
        - Recommended Authority:
        Suggest the most relevant authority to contact in order to resolve the issue.
        - Priority Level:
        Assign a priority level from 1 to 5, with 1 being maximum priority and 5 being minimum priority, to help prioritize the response to this situation based on its potential danger to people and the environment."
        If the photo does not seems to be environmental issues set the priority to -10  
        {format_instructions}
        """
        issue_parser = PydanticOutputParser(pydantic_object=issue_analysis)
        # Create a HumanMessage object with the prompt and image
        issue_message = HumanMessage(
            content=[
                {"type": "text", "text": issue_prompt.format(format_instructions=issue_parser.get_format_instructions())},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_data_b64}"},
                },
            ],
        )

        # Invoke the LLM with the message and get the response
        response = llm.invoke([issue_message])
        
        # Parse the response and extract the description, authority, and priority level
        x = issue_parser.parse(response.content)
        
        return x.description, x.title, x.authority, x.priority



