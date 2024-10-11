FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY data /app/data

RUN pip install --no-cache-dir -r requirements.txt

COPY dev_reply.py data_preprocess.py prompt.txt ./

CMD ["sh", "-c", "python data_preprocess.py && python dev_reply.py"]