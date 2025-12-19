FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run inyecta PORT=8080 automáticamente
ENV PORT=8080
EXPOSE 8080

# Usar shell form para que la variable se expanda correctamente
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]