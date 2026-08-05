# Use an official lightweight Python image
FROM python:3.12-slim

# Install LibreOffice (required for PDF generation) and clean up cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app, binding to Render's dynamic PORT environment variable
CMD sh -c "streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"