from fastapi import Depends, FastAPI, Body, HTTPException,Path,Query, Request
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
from routes.user_routes import userRouter

app=FastAPI(
    title="Aprendiendo FP",
    description="Primeros pasos de una API"

)
app.include_router(routerMovie)
app.include_router(userRouter)
Base.metadata.create_all(bind=engine)

@app.get('/',tags=['Inicio'])
def read_root():
    return HTMLResponse('<h1> Hola papu </h1>')

        





