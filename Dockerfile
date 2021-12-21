FROM python:3.8.11-slim

RUN apt-get update && \
    apt-get install -y git

EXPOSE 5000

COPY requirements/requirements.txt .

RUN pip install --upgrade -r requirements.txt --no-cache-dir

COPY ./app /app

# Default to 1 worker
ENV num_workers 1
ENV timeout 120

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5000 -w ${num_workers} -t ${timeout} -k uvicorn.workers.UvicornWorker app.main:app"]