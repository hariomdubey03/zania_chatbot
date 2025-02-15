FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache bash \
    && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "main:app", "--name", "querymind_chatbot", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=:8000", "--log-level=error", "--log-file=logs/querymind_chatbot_service.log"]

LABEL maintainer="dubeyhariom2020@gmail.com"
