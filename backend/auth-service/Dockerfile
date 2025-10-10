FROM python:3.12-slim

WORKDIR /app

COPY . .

# RUN apt-get update
# RUN apt-get install -y postgresql-client

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python3", "src/auth_service/main.py"]
