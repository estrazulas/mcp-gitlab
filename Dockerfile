FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY src/ ./src/

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

EXPOSE 8000

# De src.server:mcp.app para src.server:app
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]