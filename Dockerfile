FROM python:3.8.11-slim

RUN apt-get update && \
    apt-get install -y \
        openssh-server

EXPOSE 5000

RUN adduser --disabled-password --gecos '' api-user

WORKDIR /src

COPY requirements/requirements.txt .

RUN pip install --upgrade -r requirements.txt --no-cache-dir && \
    rm requirements.txt && \
    mkdir .multiproc && \
    chown api-user: .multiproc

COPY ./app app/
COPY ./gunicorn_conf.py .

USER api-user

RUN mkdir ~/.ssh/ && \
    touch ~/.ssh/known_hosts

# Default env variables
ENV NUM_WORKERS 1
ENV TIMEOUT 120
ENV PROMETHEUS_MULTIPROC_DIR ".multiproc"

# FIXME: Workaround to include MLFLOW_SFTP_HOST
ENV MLFLOW_SFTP_HOST localhost

CMD ["sh", "-c", "ssh-keyscan -H ${MLFLOW_SFTP_HOST} >> /home/api-user/.ssh/known_hosts ; gunicorn -b 0.0.0.0:5000 -w ${NUM_WORKERS} -t ${TIMEOUT} -c gunicorn_conf.py -k uvicorn.workers.UvicornWorker app.main:app"]