from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# --- Database setup ---
engine = create_engine("sqlite:///messages.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String)
    bot_response = Column(String)

Base.metadata.create_all(bind=engine)

# --- Routes ---
@app.get("/")
async def root():
    return {"message": "Nu Bot backend is live!"}

@app.post("/api/messages")
async def messages(request: Request):
    body = await request.json()
    user_text = body.get("text", "")
    bot_response = f"You said: {user_text}"

    # Save to DB
    db = SessionLocal()
    msg = Message(user_text=user_text, bot_response=bot_response)
    db.add(msg)
    db.commit()
    db.close()

    return JSONResponse(content={
        "type": "message",
        "text": bot_response
    })

class TestMessage(BaseModel):
    text: str

@app.post("/test/send")
async def test_send(message: TestMessage):
    return {"response": f"Echo: {message.text}"}
