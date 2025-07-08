FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN playwright install chromium
RUN playwright install-deps chromium

CMD ["gunicorn", "jobapp.wsgi:application", "--bind", "0.0.0.0:8000"]
