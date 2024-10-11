
# Overview
This is a simple project that utilizes the open-source Ollama LLM model to demonstrate its ability to help Android developers and publishers generate appropriate responses to user reviews and ratings. By integrating Ollama with a local setup, the project allows you to efficiently analyze and respond to user feedback for your Android app.

Visit my Android DEV site and my apps [here](https://play.google.com/store/apps/dev?id=5073619381401000760).

# Clone project

To get started, clone this repository to your local machine:

```git bash
git clone https://github.com/vinhDev3006/Android_Reply_LLM.git
cd Android_Reply_LLM
```

# How to run the program?

## Prerequisite
Ensure the following before proceeding:
- You have a Google Play Developer account and an app with a significant number of reviews.
- Docker / Docker Desktop is installed on your machine.
- Python is installed.


## Step 1: Set up the Ollama Model Locally
To run the Ollama LLM locally, you need to install Docker / Docker Desktop and execute the following commands:

```docker
## Pull the ollama image and run the ollama/ollama container in GPU mode.
docker run --rm --gpus=all -d -v ollama_data:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

## Test llama3.2:latest model
docker exec -it ollama ollama run llama3.2:latest
```

## Step 2: Download Review Dataset
You can download the review dataset from your Google Play Console. Navigate to your app's page and export the review reports.

![Review Report](/doc/doc_img_1.png)

Once downloaded, place the dataset in the data/ folder.

## Step 3: Install Python Dependencies
To install the required Python packages, preferrably in a virtual environment, run:

```bash
pip install -r requirements.txt
```

## Step 4: Pre-process Review Data
Change the input file path to the file that you pre-processed. Finally, run the script that processes user reviews and generates appropriate responses using the Ollama model:

```bash
python data_preprocess.py
```

## Step 5: Generate Developer Replies

Change the input file path to the file that you pre-processed.
Finally, run the script that processes user reviews and generates appropriate responses using the Ollama model:

```bash
python dev_reply.py
```

This script will automatically analyze the reviews and output suggested responses in a suitable format.

![Output](/doc/doc_img_2.png)


# Future improvement and contribution

The current project only outputs developer replies as plain text in the terminal. Future improvement can include something like integration with the Google Play Console API to automatically post replies.

Feel free to contribute to this project by opening pull requests or submitting issues. We welcome feedback and suggestions to improve the performance and functionality of this tool.

# Extra
This project includes a Dockerfile and a docker-compose.yml to facilitate easy setup and deployment. It is recommended to use Docker Desktop.

```docker
cd Android_Reply_LLM

docker compose build
docker compose up
```

For more details on the Docker configuration, please refer to the docker-compose.yml file in this repository.
