FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Clone model repository
RUN git clone https://github.com/fashn-AI/fashn-vton-1.5.git /app/fashn-vton

WORKDIR /app/fashn-vton

RUN pip install -e .

# Download model weights during build
RUN python scripts/download_weights.py \
    --weights-dir /app/weights

WORKDIR /app

COPY handler.py .
COPY model.py .
COPY utils.py .

CMD ["python", "-u", "handler.py"]
