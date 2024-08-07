FROM python:3.12.1

RUN mkdir /fastapi_chat_app

WORKDIR /fastapi_chat_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000




