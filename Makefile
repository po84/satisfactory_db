dev_local:
	uvicorn main:app --reload

dev_lan:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
