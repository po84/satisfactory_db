- **Create a virtual environment and activate it:**
```bash
python -m venv venv
source venv/bin/activate
```

- **Deactivate an active virtual environment:**
```bash
deactivate
```

- **Create or update a requirements file:**
```bash
pip freeze > requirements.txt
``` 

- **Install package from a requirements file:**
```bash
pip install -r requirements.txt
```

- **Start server:**
```bash
uvicorn main:app --reload
```