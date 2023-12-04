FROM python:3.6.8

RUN pip install --upgrade pip

WORKDIR /bert_flask_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "bert_flask_service.py", "/home/dasha/docker-k8s-test/bert_flask_service/model_save_v2_10k_20e", "/home/dasha/datasets"]
