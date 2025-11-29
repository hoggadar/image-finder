FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

CMD ["python", "src/vector_loader_service/main.py"]

