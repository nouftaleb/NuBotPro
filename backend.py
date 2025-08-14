from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Nu Bot backend is live!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/env")
def get_env():
    secret = os.getenv("MY_SECRET", "Not set")
    return {"MY_SECRET": secret}
