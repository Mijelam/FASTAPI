import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db.database import Base, get_db
import os

#  Configuración de la Base de Datos de Prueba

# Usar una base de datos SQLite en memoria para los tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.sqlite"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear una sesión de prueba que los tests usarán
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

#  2. Sobrescribir la Dependencia get_db


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


#  3. Fixture de Pytest

@pytest.fixture(scope="function")
def client():

    # Aquí cambiamos el anterior  get_db por el que acabamos de crear
    app.dependency_overrides[get_db] = override_get_db

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Proporciona el cliente de prueba
    yield TestClient(app)

    # Limpia lo que sobreescribimos
    app.dependency_overrides = {}

    # Elimina todas las tablas
    Base.metadata.drop_all(bind=engine)

    # cierra todas las conexiones
    engine.dispose()

    # elimina la  db
    if os.path.exists("test.sqlite"):
        os.remove("test.sqlite")


# 4. Tests

def test_register_user(client: TestClient):

    # 1. Registro de un usuario
    response = client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "newpw"})

    # 2. Verificacion del estado devuelto y el mensaje, junto con mensaje diagnostico por si  falla
    assert response.status_code == 201, response.tex
    assert response.json()["message"] == "usuario creado correctamente"


def test_register_existing_user(client: TestClient):

    # 1. Registro de un usuario
    client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "pw"})

    # 2. Intento de registro  del mismo usuario
    response = client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "pw"})

    # 3. Verificación
    assert response.status_code == 404, response.text
    assert "Email ya registrado" in response.json()["detail"]
