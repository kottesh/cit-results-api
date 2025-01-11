FROM python:3.13-alpine

EXPOSE 7475
WORKDIR /app

RUN apk --update add redis

COPY requirements .
RUN pip install --no-cache-dir -r requirements

COPY . .

RUN echo '#!/bin/sh' > /run.sh && \
    echo 'redis-server --daemonize yes' >> /run.sh && \
    echo 'gunicorn -w 4 --bind 0.0.0.0:7475 app:app' >> /run.sh && \
    chmod +x /run.sh

CMD ["/run.sh"]
