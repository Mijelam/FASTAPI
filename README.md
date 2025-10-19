# Movie Manager API

This is a REST API for managing movies. I made it with FastAPI and SQLAlchemy while learning backend stuff.  
You can create, read, update, and delete movies, and also register/login users with JWT tokens.

## Features

* **CRUD for Movies:** Add, see, edit, and delete movies.  
* **User Auth:** Login and get a token to use the movie endpoints.  
* **Database:** Uses SQLite with SQLAlchemy.  
* **Validation:** Uses Pydantic to check the data.  
* **Testing:** Some tests with pytest.  
* **Docker:** Includes a `dockerfile` to run it in a container

## Tech Used

* FastAPI  
* SQLAlchemy  
* Pydantic  
* PyJWT  
* Bcrypt  
* Uvicorn  
* Pytest 

## API Endpoints

### Authentication

*   `POST /login`: Authenticate a user and receive a JWT token.
*   `POST /register`: Register a new user.

### Movies

*   `GET /movies`: Get a list of all movies.
*   `GET /movies/{id}`: Get a movie by its ID.
*   `GET /movies/?category={category}`: Get movies by category (Query Parameter).
*   `POST /movies`: Create a new movie.
*   `PUT /movies/{id}`: Update an existing movie.
*   `DELETE /movies/{id}`: Delete a movie.

## Deployment
The FastAPI application was deployed on an EC2 instance with HTTPS enabled.  

- NGINX was used as a **reverse proxy** to forward requests to the FastAPI app running in a container.  
- A free domain was created using **No-IP** (`moviesapi.ddns.net`).  
- **Certbot** with Let's Encrypt was used to generate a free SSL certificate for HTTPS.  
- AWS Security Group rules were updated to allow traffic on **ports 80 (HTTP) and 443 (HTTPS)**.  

After this setup, the API is accessible securely at:
[API Documentation](https://moviesapi.ddns.net/docs)


