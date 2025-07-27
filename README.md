# FastAPI Practice Project 

This is just a small **practice project** to explore how FastAPI works.

You'll quickly notice it's not meant for production  for example, the JWT token is encoded like this:

```python
token: str = encode(payload=data, key='Holi', algorithm='HS256')
```

Yes. `'Holi'` is the secret key.   
this was just for testing authentication using **JWT**.

---

##  What was the goal?

- Test basic JWT authentication and how request headers work in FastAPI.
- Use **SQLAlchemy** ORM, **Pydantic** and understand how it differs from Django REST Framework.
- Deploy a simple FastAPI app in a Docker container on AWS EC2.

---

##  FastAPI vs Django REST

Coming from Django REST, some differences were immediately noticeable:

- In **Django REST**, you define a **serializer**, link it to a model and data, and use `partial=True` to update only the fields you need..
- In **FastAPI**, you need to:
  - Create a **separate Pydantic model** for updates. (You might say this is good because it follows the **S** in **SOLID**, but...)
  - Convert the request body to a dictionary.
  - Manually iterate over the fields and update them one by one.

Example:

```python
update_data = movie_update.model_dump(exclude_unset=True)
for key, value in update_data.items():
    setattr(movie, key, value)
```
-More stuff


---

##  Docker + Deployment

The project was deployed on an **EC2 instance using Docker**.  


---
