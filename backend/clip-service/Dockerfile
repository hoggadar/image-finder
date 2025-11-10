FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python3", "src/clip_service/main.py"]
