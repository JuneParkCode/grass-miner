FROM python:3.9-alpine

RUN apk add --no-cache chromium chromium-chromedriver unzip

WORKDIR /app

COPY ./src/requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src .

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]

EXPOSE 80