FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124 \
    && python3 -m pip install -r requirements.txt

COPY src/ ./src/
COPY models/best.pt ./models/best.pt

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "sightline.api:app", "--host", "0.0.0.0", "--port", "8000"]
