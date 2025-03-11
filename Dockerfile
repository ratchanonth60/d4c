FROM python:3.12-slim

WORKDIR /fast-api/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH="/fast-api/app"

# Copy the entire app directory
COPY ./app /fast-api/app

# Set PYTHONPATH to ensure imports work correctly
ENV PYTHONPATH="/fast-api"


# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
