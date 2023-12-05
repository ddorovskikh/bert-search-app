FROM python:3.6.8

ENV FLASK_PATH=/data BERT_MODEL=/model

RUN pip install --upgrade pip

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "bert_flask_service.py"]
