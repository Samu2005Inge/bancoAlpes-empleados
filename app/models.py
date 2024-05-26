from pydantic import BaseModel, Field, EmailStr
from app.database import Base
from sqlalchemy import Column, Integer, String


class Empleado(Base):
    __tablename__ = "empleados"

    name = Column(String(50), nullable=True)
    username = Column(String(50), unique=True, nullable=True, default=None)
    email = Column(String(254), primary_key=True, default=None)
    password = Column(String(50), nullable=True, default=None)
    role = Column(String(50), nullable=True)

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


class UsedAccessToken(Base):
    __tablename__ = "used_access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJkdWxhemVleiJ9.1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI1zV3j2e3ZpI",
            }
        }