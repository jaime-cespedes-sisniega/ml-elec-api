serve-dev:
	uvicorn api.main:api --host 0.0.0.0 --port 5000 --workers 1

serve-prod:
	gunicorn -b 0.0.0.0:5000 -w 5 -k uvicorn.workers.UvicornWorker api.main:api # Num workers = (2*CPU) + 1

build:
	docker build -t ml-elec-api .

run:
	docker run -d --name ml-elec-api -p 80:5000 -e num_workers=5 ml-elec-api # Num workers = (2*CPU) + 1