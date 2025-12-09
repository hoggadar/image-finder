FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Disable hf_xet downloader to use standard downloader with proper progress bar
# Model will be downloaded on first container startup, not during build
ENV HF_HUB_DISABLE_XET=1
ENV HF_HUB_ENABLE_HF_TRANSFER=0

CMD ["python3", "src/clip_service/main.py"]
