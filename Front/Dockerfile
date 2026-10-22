FROM node:22-bookworm-slim AS frontend

WORKDIR /app/Front
COPY Front/package*.json ./
RUN npm ci
COPY Front/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision
COPY Front/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENV TORCH_HOME=/opt/torch
RUN mkdir -p /opt/torch/hub \
    && printf '%s\n' rwightman_gen-efficientnet-pytorch > /opt/torch/hub/trusted_list
RUN python -c "import torch; torch.hub.load('intel-isl/MiDaS', 'MiDaS_small', trust_repo=True); torch.hub.load('intel-isl/MiDaS', 'transforms', trust_repo=True)"
COPY main.py ./main.py
COPY depth.py ./depth.py
COPY Front/server.py ./server.py
COPY --from=frontend /app/Front/dist ./dist

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python", "server.py"]
