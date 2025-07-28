import bcrypt
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from db.database import get_db
from sqlalchemy.orm import Session
from JWT import createToken
from models.user import User as modelUser


userRouter = APIRouter()


class User(BaseModel):
    email: str
    password: str


@userRouter.post('/login', tags=['Authentication'])
def login(user: User, db: Session = Depends(get_db)):

    db_user = db.query(modelUser).filter(modelUser.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Email no registrado")

    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token_data = {"id": db_user.id, "email": db_user.email}
    token: str = createToken(token_data)

    return JSONResponse(content={"token": token})


@userRouter.post('/register', tags=['Register'])
def register(user: User, db: Session = Depends(get_db)):

    data = db.query(modelUser).filter(
        modelUser.email == user.email).first()
    if data:
        raise HTTPException(status_code=404, detail="Email ya registrado")
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user.password = hashed_password
    newUser = modelUser(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return JSONResponse(status_code=201, content={'message': 'usuario creado correctamente'})
