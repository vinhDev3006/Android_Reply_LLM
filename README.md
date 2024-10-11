 docker run --rm --gpus=all -d -v ollama_data:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
 docker exec -it ollama ollama run llama3.2:latest