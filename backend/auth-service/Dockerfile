FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir --upgrade pip setuptools poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
RUN rm -rf $(poetry config cache-dir)/{cache,artifacts}

CMD ["python3", "src/auth_service/main.py"]
