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

def test_registrar_user(client: TestClient):

    # 1. Registro de un usuario
    response = client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "newpw"})

    # 2. Verificacion del estado devuelto y el mensaje, junto con mensaje diagnostico por si  falla
    assert response.status_code == 201, response.tex
    assert response.json()["message"] == "usuario creado correctamente"


def test_registrar_user_existente(client: TestClient):

    # 1. Registro de un usuario
    client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "pw"})

    # 2. Intento de registro  del mismo usuario
    response = client.post(
        "/register", json={"email": "newuser@gmail.com", "password": "pw"})

    # 3. Verificación
    assert response.status_code == 404, response.text
    assert "Email ya registrado" in response.json()["detail"]


# Principalmente para probar el funcionamiento de Next.
def test_usar_get_movies(client: TestClient):
    # 1. Registro de un usuario
    client.post(
        "/register", json={"email": "user@gmail.com", "password": "1234"})

    # 2. Hacer login y obtener el token
    login_response = client.post(
        "/login", json={"email": "user@gmail.com", "password": "1234"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]  # la clave donde esta el Token

    # 3. Insertar una peli para verificar contenido
    # Forzar a que nos devuelva el yield con la nueva sesion
    db = next(override_get_db())
    from models.movie import Movie
    db.add(Movie(title="Test Movieeee", overview="A short overviewww",
           rating=4.5, year=2024, category="Adventureeee"))
    db.commit()

    # 4. Llamar a /movies con el token en el header
    response = client.get(
        "/movies", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    movies = response.json()
    # verificar que nos devuelve una lista con las peliculas
    assert isinstance(movies, list)
    # verificar si esta la pelicula, como solo hay una, su id será 1.
    assert any(m["id"] == 1 for m in movies)


def test_usar_create_movies(client: TestClient):
    # 1. Registro de un usuario
    client.post(
        "/register", json={"email": "user@gmail.com", "password": "1234"})

    # 2. Hacer login y obtener el token
    login_response = client.post(
        "/login", json={"email": "user@gmail.com", "password": "1234"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]  # la clave donde esta el Token

    # 3. Crear película usando el token
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Inception",
            "overview": "Dreams within dreams",
            "rating": 9,
            "year": 2010,
            "category": "Science Fiction"
        }
    )
    assert response.status_code == 200
    assert response.json()["movie"]["title"] == "Inception"


def test_usar_get_movies_diferente(client: TestClient):
    # 1. Registro de un usuario
    client.post(
        "/register", json={"email": "user@gmail.com", "password": "1234"})

    # 2. Hacer login y obtener el token
    login_response = client.post(
        "/login", json={"email": "user@gmail.com", "password": "1234"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]  # la clave donde esta el Token

    # 3. Crear película usando el token
    response = client.post(
        "/movies",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Inception",
            "overview": "Dreams within dreams",
            "rating": 9,
            "year": 2010,
            "category": "Science Fiction"
        }
    )
    # 4. Llamar a /movies con el token en el header
    response = client.get(
        "/movies", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    movies = response.json()
    # verificar que nos devuelve una lista con las peliculas
    assert isinstance(movies, list)
    # verificar si esta la pelicula, como solo hay una, su id será 1.
    assert any(m["id"] == 1 for m in movies)
