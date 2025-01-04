FROM python:3.13-alpine
EXPOSE 5000 
WORKDIR /app
COPY requirements .
RUN pip install -r requirements
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
