dev_local:
	uvicorn app.main:app --reload

dev_lan:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
