from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
import os
from sqlalchemy import JSON
import uvicorn
from JWT import createToken, validateToken
from models.movie import Movie as modelMovie
from db.database import engine, Session, Base
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from routes.movie_routes import routerMovie
from routes.user_routes import userRouter

app = FastAPI(
    title="Documentacion automatica",
    description="endpoints",
     openapi_tags=[
        {
            "name": "Movies",
            "description": "Funciones CRUD para las peliculas."
        },
        {
            "name": "Authentication",
            "description": "Inicio de sesión y creación del Token."
        },
        {
            "name": "Register",
            "description": "Registro del usuario"
        }
    ]

)
app.include_router(routerMovie)
app.include_router(userRouter)
Base.metadata.create_all(bind=engine)


@app.get('/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h1> Hola desde EC2 </h1>')


if __name__ == ' __ main __ ':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
