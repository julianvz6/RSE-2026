FROM python:3.10-slim

LABEL maintainer="julianvz6"
LABEL description="Individual Assesment 1 - PDF Article Analysis Pipeline"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY setup.cfg .
COPY config.json .
COPY grobid_output/ ./grobid_output/
COPY articles/ ./articles/

RUN mkdir -p prac_output

CMD ["python", "main.py"]
