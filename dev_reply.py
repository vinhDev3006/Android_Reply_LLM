import json
import os

import httpx
import ollama
import pandas as pd

# OLLAMA CONFIGURATION
OLLAMA_CONNECTION_STR = os.environ.get("OLLAMA_CONNECTION_STR", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
PROMPT_TEMPLATE_PATH = os.environ.get("PROMPT_TEMPLATE_PATH", "prompt.txt")


# DATA PROCESSING
file_path = os.path.join("data", "october_reviews_record.csv")
df = pd.read_csv(file_path, encoding="utf-8")
df = df[["Star Rating","Review Text"]]
df = df.dropna()
df = df.astype(str)


# WAIT FOR OLLAMA SERVER TO BE CONNECTED
def wait_for_ollama(ollama_client: ollama.Client):
    while True:
        try:
            ollama_client.ps()
            break
        except httpx.HTTPError as exc:
            print(f"HTTP Exception for {exc.request.url} - {exc}")


# DOWNLOAD THE PREFERRED OLLAMA MODEL IF NOT AVAILABLE LOCALLY
def download_model(ollama_client: ollama.Client, model: str):
    existing_models = [model["name"] for model in ollama_client.list()["models"]]
    if model not in existing_models:
        print(f"Model not found locally, downloading: {model}")
        ollama_client.pull(model)
    else:
        print(f"Model: {model} found locally")


# FUNCTIONS THAT UTILIZE THE PROMPT AND RETURN THE RESPONSE JSON 
def dev_reply_agent(
    review: str,
    rating: str,
    prompt_template: str, 
    ollama_client: ollama.Client
) -> str:
    review = review.replace('"', "'")
    rating = rating.replace('"', "'")
    prompt = prompt_template
    
    prompt = prompt.replace("$REVIEW", review)
    prompt = prompt.replace("$RATING", rating)
    

    api_response = ollama_client.generate(
        model=OLLAMA_MODEL,
        prompt=prompt,
        format="json",
        stream=False,
    )

    response = api_response["response"]
    data = json.loads(response)
    developer_reply = data["developer_reply"]

    return developer_reply


def main():
    ollama_client = ollama.Client(host=OLLAMA_CONNECTION_STR)
    wait_for_ollama(ollama_client)
    download_model(ollama_client, OLLAMA_MODEL)
    
    with open(file=PROMPT_TEMPLATE_PATH, mode='r', encoding="utf8") as file:
        prompt_template = file.read()
    user_reviews = df

    for index, row in user_reviews.iterrows():
        developer_reply = dev_reply_agent(
            review = row.iloc[1],
            rating = row.iloc[0],
            prompt_template=prompt_template,
            ollama_client=ollama_client
        )

        print(f"{int(row.iloc[0]) * "⭐"}\nUSER: {row.iloc[1]}\nDEVELOPER: {developer_reply}\n\n")
        

if __name__ == "__main__":
    main()