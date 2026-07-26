# Module 11 - FastAPI Calculator

## Description

This project is a FastAPI Calculator application that demonstrates:

- SQLAlchemy database models
- Pydantic data validation
- Factory Pattern
- Unit, Integration, and End-to-End testing
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

Open:

```
http://127.0.0.1:8000
```

---

## Running Tests

Run all tests:

```bash
python -m pytest -v
```

Run unit tests:

```bash
python -m pytest tests/unit -v
```

Run integration tests:

```bash
python -m pytest tests/integration -v
```

Run end-to-end tests:

```bash
python -m pytest tests/e2e -v
```

---

## Docker Hub Repository

https://hub.docker.com/r/juhip25/module8_is601

---

## GitHub Repository

https://github.com/juhip2505-cpu/module8_is601