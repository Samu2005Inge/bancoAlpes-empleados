import time
from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from http.client import HTTPResponse
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt, decode_jwt
from app.schemas import EmpleadoLoginSchema, UsedAccessTokenSchema, EmpleadoSchema

from sqlalchemy.orm import Session

import hashlib

from . import models

from app.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]


app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
        



def get_user_by_email(email: str, db: Session):
    return db.query(models.Empleado).filter(models.Empleado.email == email).first()


def hash_password(password: str):
    password = password.encode("utf-8")
    hash_object = hashlib.sha256(password)
    hex_dig = hash_object.hexdigest()
    return hex_dig



def check_user(data: EmpleadoLoginSchema, db: Session):
    usuario = get_user_by_email(data.email, db)
    password_data = hash_password(data.password)
    if usuario:
        if usuario.password == password_data:
            return True
    return False


@app.post("/empleado/login", response_model=None , tags=["empleado"])
async def user_login(user: EmpleadoLoginSchema = Body(...), db: Session = Depends(get_db)):
    if check_user(user, db):
        return sign_jwt(user.email)
    return {
        "error": "Wrong login details!"
    }


@app.get("/empleado/is_authenticated", tags=["empleado"])
async def is_authenticated(token: str, db: Session = Depends(get_db)):
    email = decode_jwt(token)

    tokens_usados = db.query(models.UsedAccessToken).all()
    token_modelo_usado = False

    for token_usado in tokens_usados:
        if token == token_usado.token:
            token_modelo_usado = True


    if email and not token_modelo_usado:
        return {
            "data": "User is authenticated."
        }
    return {
        "error": "User is not authenticated."
    }


@app.get("/empleado/info", tags=["empleado"])
async def empleado_info(token: str, db: Session = Depends(get_db)):
    email = decode_jwt(token)['user_id']

    if email:
        return {
            "data": get_user_by_email(email, db)
        }
    return {
        "error": "User is not authenticated."
    }


@app.get("/empleado/logout", tags=["user"])
async def empleado_logout(token: str, db: Session = Depends(get_db)):

    # Agregar el token a la base de datos de tokens usados
    token_model = models.UsedAccessToken(token=token)
    db.add(token_model)
    db.commit()
    db.refresh(token_model)
    return {
        "data": "User has been logged out."
    }
@app.get("/health-check", tags=["root"])
def health_check():
    return JSONResponse(status_code=200, content={"message": "OK"})
