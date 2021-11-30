.ONESHELL:
SHELL := /bin/bash

VENV=.venv

install:
	python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	pip3 install --upgrade pip &&\
				 pip3 install -r requirements/requirements.txt \
				              -r requirements/tox_requirements.txt

tox:
	$(VENV)/bin/tox

serve-dev:
	uvicorn api.main:api --host 0.0.0.0 --port 5000 --workers 1

serve-prod:
	gunicorn -b 0.0.0.0:5000 -w 5 -k uvicorn.workers.UvicornWorker api.main:api

build:
	docker build -t ml-elec-api .

run:
	docker run -d --name ml-elec-api -p 80:5000 -e num_workers=5 ml-elec-api