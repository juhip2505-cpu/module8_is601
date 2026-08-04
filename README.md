# Module 13 - JWT Authentication FastAPI Calculator

## Description

This project is a FastAPI Calculator application that demonstrates:

- JWT Authentication
- User Registration and Login
- Password Hashing
- SQLAlchemy database models
- Pydantic data validation
- Protected API endpoints
- Unit, Integration, and End-to-End (Playwright) testing
- GitHub Actions CI/CD
- Docker deployment

---

## Running the Application

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open the application:

```
http://127.0.0.1:8000
```

---

## Authentication Pages

Registration:

```
http://127.0.0.1:8000/register-page
```

Login:

```
http://127.0.0.1:8000/login-page
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit -v
```

Run integration tests:

```bash
pytest tests/integration -v
```

Run Playwright end-to-end tests:

```bash
pytest tests/e2e -v
```

---

## Docker Hub Repository

https://hub.docker.com/r/juhip25/module8_is601

---

## GitHub Repository

https://github.com/juhip2505-cpu/module8_is601