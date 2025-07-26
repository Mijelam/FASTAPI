from fastapi import Depends, FastAPI, Body, HTTPException,Path,Query, Request,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel,Field
from  typing import Optional

from sqlalchemy import JSON
from JWT import createToken, validateToken
from models.movie import Movie as modelMovie
from db.database import  engine,Session,Base
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from routes.movie_routes import  routerMovie

userRouter=APIRouter()

class User(BaseModel):
    email:str
    password:str



@userRouter.post('/login',tags=['Authentication'])
def login(user:User):
    if user.email=="holo@gmail.com" and user.password=="123":
        token:str=createToken(user.model_dump())
        print(token)
        return token
    raise HTTPException(status_code=403,detail="Acceso denegado")