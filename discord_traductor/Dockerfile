FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN python3 -m pip install --upgrade pip
RUN pip install -U python-dotenv 
RUN pip install googletrans==3.1.0a0
RUN pip install pika

ENV PYTHONUNBUFFERED=TRUE

COPY . discord_traductor/

CMD ["python","discord_traductor/traductor.py"]
