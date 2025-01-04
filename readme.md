# cit-results-api

```
$ docker build -t cit-results-api .
$ docker run -dp 8485:5000 -v "$(pwd):/app" --name cit-results-api cit-results-api:latest
```

open `localhost:8485` where you could test the api.
