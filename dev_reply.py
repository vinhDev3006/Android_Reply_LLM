# dev_reply.py

import json
import os
import httpx
import ollama
import pandas as pd
import argparse

# OLLAMA CONFIGURATION
OLLAMA_CONNECTION_STR = os.environ.get(
    "OLLAMA_CONNECTION_STR", "http://localhost:11434"
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
PROMPT_TEMPLATE_PATH = os.environ.get("PROMPT_TEMPLATE_PATH", "prompt.txt")

# DATA PROCESSING
parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--data",
    help="Location to save the processed data",
    type=str,
    default=os.path.join("data", "october_reviews_record.csv"),
)
args = parser.parse_args()

file_path = args.data

try:
    df = pd.read_csv(file_path, encoding="utf-8")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except pd.errors.EmptyDataError:
    print(f"Error: File '{file_path}' is empty.")
    exit()
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()

df = df[["Star Rating", "Review Text"]].dropna().astype(str)


# WAIT FOR OLLAMA SERVER TO BE CONNECTED
def wait_for_ollama(ollama_client: ollama.Client):
    while True:
        try:
            ollama_client.ps()
            print("Ollama server connected.")
            break
        except httpx.HTTPError as exc:
            print(f"HTTP Exception for {exc.request.url} - {exc}")
            print("Retrying to connect to Ollama server...")
            continue


# DOWNLOAD THE PREFERRED OLLAMA MODEL IF NOT AVAILABLE LOCALLY
def download_model(ollama_client: ollama.Client, model: str):
    existing_models = [model["name"] for model in ollama_client.list()["models"]]
    if model not in existing_models:
        print(f"Model not found locally, downloading: {model}")
        ollama_client.pull(model)
    else:
        print(f"Model: {model} found locally.")


# FUNCTION THAT USES THE PROMPT AND RETURNS THE RESPONSE JSON
def dev_reply_agent(
    review: str, rating: str, prompt_template: str, ollama_client: ollama.Client
) -> str:
    review = review.replace('"', "'")
    rating = rating.replace('"', "'")
    prompt = prompt_template.replace("$REVIEW", review).replace("$RATING", rating)

    try:
        api_response = ollama_client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            format="json",
            stream=False,
        )

        response = api_response.get("response")
        if response:
            data = json.loads(response)
            developer_reply = data.get("developer_reply", "No reply generated.")
        else:
            developer_reply = "No response from API."
    except json.JSONDecodeError:
        developer_reply = "Failed to decode JSON response."
    except Exception as e:
        developer_reply = f"Error occurred: {e}"

    return developer_reply


def main():
    ollama_client = ollama.Client(host=OLLAMA_CONNECTION_STR)
    wait_for_ollama(ollama_client)
    download_model(ollama_client, OLLAMA_MODEL)

    try:
        with open(file=PROMPT_TEMPLATE_PATH, mode="r", encoding="utf8") as file:
            prompt_template = file.read()
    except FileNotFoundError:
        print(f"Error: Prompt template file '{PROMPT_TEMPLATE_PATH}' not found.")
        exit()

    user_reviews = df

    # Iterate through reviews and generate developer replies
    for index, row in user_reviews.iterrows():
        try:
            developer_reply = dev_reply_agent(
                review=row["Review Text"],
                rating=row["Star Rating"],
                prompt_template=prompt_template,
                ollama_client=ollama_client,
            )
            print(
                f"{'⭐' * int(row['Star Rating'])}\nUSER: {row['Review Text']}\nDEVELOPER: {developer_reply}\n\n"
            )
        except Exception as e:
            print(f"Error processing review at index {index}: {e}")


if __name__ == "__main__":
    main()
