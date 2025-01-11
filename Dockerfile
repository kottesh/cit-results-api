FROM python:3.13-alpine

EXPOSE 7475
WORKDIR /app

RUN apk --update add redis

COPY requirements .
RUN pip install --no-cache-dir -r requirements

COPY . .

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:7475", "app:app"]
