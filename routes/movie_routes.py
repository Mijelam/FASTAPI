from fastapi import Depends, HTTPException, Path, Query, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from db.database import get_db
from JWT import validateToken
from models.movie import Movie as modelMovie
from sqlalchemy.exc import NoResultFound

routerMovie = APIRouter()


class Movie(BaseModel):
    title: str = Field(default="Title of the movie",
                       min_length=8, max_length=60)
    overview: str = Field(default="Description of the movie",
                          min_length=8, max_length=60)
    rating: float = Field(ge=1, le=10)
    year: int = Field(default=2024)
    category: str = Field(default="category of the movie",
                          min_length=8, max_length=60)


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    category: Optional[str] = None


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):

        auth = await super().__call__(request)
        if auth is None or auth.credentials is None:
            raise HTTPException(
                status_code=403, detail="Token no proporcionado")
        data = validateToken(auth.credentials)


@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies(db: Session = Depends(get_db)):
    data = db.query(modelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.get('/movies/{id}', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movie(id: int = Path(ge=0), db: Session = Depends(get_db)):
    try:
        data = db.query(modelMovie).filter(modelMovie.id == id).one()
        return JSONResponse(content=jsonable_encoder(data))
    except NoResultFound:
        return JSONResponse(content="Esa peli no existe")


@routerMovie.get('/movies/', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movie_by_category(category: str = Query(min_length=8, max_length=60), db: Session = Depends(get_db)):
    data = db.query(modelMovie).filter(modelMovie.category == category).all()
    if not data:
        return JSONResponse(content="Esa categoria no existe ")

    return JSONResponse(content=jsonable_encoder(data))


@routerMovie.post('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def create_movies(movie: Movie, db: Session = Depends(get_db)):

    newMovie = modelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()

    return JSONResponse(content={'Message': 'Se ha creado la pelicula', 'movie': movie.model_dump()})


@routerMovie.patch('/movies/{id}', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def update_movie(id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):

    try:
        data = db.query(modelMovie).filter(modelMovie.id == id).one()

    # Actualiza solo los campos que vienen en el request
        update_data = movie_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(data, key, value)

        db.commit()
        return JSONResponse(content={"message": "Pelicula correctamente actualizada"})
    except NoResultFound:
        return JSONResponse(content="Esa  pelicula  no  existe")


@routerMovie.delete('/movies/{id}', tags=['Movies'], status_code=204, dependencies=[Depends(BearerJWT())])
def delete_movie(id: int, db: Session = Depends(get_db)):

    try:
        data = db.query(modelMovie).filter(modelMovie.id == id).one()
        db.delete(data)
        db.commit()
        return JSONResponse(content={'Message': 'Borrado exitosamente'})

    except NoResultFound:
        return JSONResponse(content="Esa pelicula no existe ")
