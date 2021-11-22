serve-dev:
	uvicorn api.main:api --host 0.0.0.0 --port 5000 --workers 5  # Num workers = (2*CPU) + 1