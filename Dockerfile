FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Clone FASHN VTON
RUN git clone https://github.com/fashn-AI/fashn-vton-1.5.git /app/fashn-vton

WORKDIR /app/fashn-vton

RUN pip install -e .

WORKDIR /app

COPY handler.py .
COPY model.py .
COPY utils.py .

CMD ["python", "-u", "handler.py"]
