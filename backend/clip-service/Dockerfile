FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Pre-download CLIP model during build (with progress bar)
ENV HF_HUB_ENABLE_HF_TRANSFER=0
RUN python -c "\
import logging; \
logging.basicConfig(level=logging.INFO); \
from transformers import CLIPModel, CLIPProcessor; \
print('Downloading CLIP model...'); \
CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); \
print('Downloading CLIP processor...'); \
CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32'); \
print('Done!')"

CMD ["python3", "src/clip_service/main.py"]
