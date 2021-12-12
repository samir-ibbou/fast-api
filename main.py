import os

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.db.models import UserAnswer
from app.api import api

os.environ["TZ"] = "UTC"
title_detail = os.getenv("PROJECT_ID", "Local")
version = os.getenv("SHORT_SHA", "local")

CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Invalid credentials.",
                                      headers={"WWW-Authenticate": "Bearer"})

app = FastAPI(title=f"CloudRun FastAPI: {title_detail}", version=version)


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/user")
def read_user():
    return api.read_user()


@app.get("/question/{position}", status_code=200)
def read_questions(position: int):
    question = api.read_questions(position)

    if not question:
        raise HTTPException(status_code=400, detail="Error")

    return question


@app.get("/alternatives/{question_id}")
def read_alternatives(question_id: int):
    return api.read_alternatives(question_id)


@app.post("/answer", status_code=201)
def create_answer(payload: UserAnswer):
    payload = payload.dict()

    return api.create_answer(payload)


@app.get("/result/{user_id}")
def read_result(user_id: int):
    return api.read_result(user_id)
