"""
Satisfactory DB Backend
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():
    """Test Endpoint"""
    return {"Hello": "How are you doing?"}
