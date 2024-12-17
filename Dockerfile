FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src src
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]