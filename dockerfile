FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice libreoffice-script-provider-python python3-uno && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Use our startup script to run both Flask and Streamlit
CMD ["./start.sh"]
