from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.prompts import PromptTemplate
import getpass

from dotenv import load_dotenv
import os
import toml

import streamlit


# SET UP CONFIGURATION
load_dotenv()

current_directory = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_directory, "config", "google_gemini_model.toml")

with open(config_path, "r") as f:
    config = toml.load(f)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


# DEFINE MODEL
llm = ChatGoogleGenerativeAI(
    model=config["model"]["name"],
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    },
)

# DEFINE PROMPT
prompt = PromptTemplate(
    input_variables=["review", "rating"],
    template="What is the best response to this user’s review and rating of my mobile app, considering the following details: {review} and {rating}? Ensure the response is cheerful yet professional, using the same language as the user's review, and include emojis if necessary.",
)

chain = prompt | llm

# WEB APP
streamlit.title("WHAT TO REPLY?")
review = streamlit.text_input("Input user's review:")
rating = streamlit.number_input("Input user's rating", max_value=5, min_value=1)

if review and rating:
    response = chain.invoke({"rating": rating, "review": review})
    streamlit.write(response.content)
