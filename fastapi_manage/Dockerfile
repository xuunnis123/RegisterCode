FROM tiangolo/uvicorn-gunicorn:python3.8
#python:3.8-slim-buster

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]