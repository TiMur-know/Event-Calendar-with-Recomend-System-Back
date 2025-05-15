FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy

EXPOSE 5000

USER demouser

CMD ["python", "run.py"]
