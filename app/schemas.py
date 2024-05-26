from pydantic import BaseModel, Field, EmailStr
from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

#class PostSchema(BaseModel):
    #id: int = Field(default=None)
    #title: str = Field(...)
    #content: str = Field(...)

    #class Config:
       # json_schema_extra = {
            #"example": {
                #"title": "Securing FastAPI applications with JWT.",
                #"content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            #}
        #}


class EmpleadoSchema(BaseModel):

    name: str = Field(None, max_length=50)
    username: str = Field(None, max_length=50)
    email: EmailStr
    password: str = Field(None, max_length=50)
    role: str = Field(None, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jhon",
                "username": "Empleado1",
                "email": "abdulazeez@x.com",
                "password": "weakpassword",
                "role": "asesor"
            }
        }


class EmpleadoLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

class UsedAccessTokenSchema(BaseModel):
    id: int = Field(default=None)
    token: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJkdWxhemVleiJ9.1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI",
            }
        }