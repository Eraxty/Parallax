FROM node:22-bookworm-slim AS frontend

WORKDIR /app/Front
COPY Front/package*.json ./
RUN npm ci
COPY Front/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app
COPY Front/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py ./main.py
COPY Front/server.py ./server.py
COPY --from=frontend /app/Front/dist ./dist

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python", "server.py"]
