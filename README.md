### This repository contains CRUD FastAPI project for todo app and TESTS

What's used for this project:
1. FastAPI - to create API endpoints
2. Swagger - API documentation http://127.0.0.1:8000/docs & OpenAPI specification JSON format http://127.0.0.1:8000/openapi.json
3. ReDoc - alternative API documentation http://127.0.0.1:8000/redoc
4. Pydantic - data validation for API calls (request & response)
5. Pytest - tests coverage

To run project locally execute `fastapi dev src`

**Tests**:
1. To run tests `pytest`
2. To get general test coverage run `pytest --cov` & detailed coverage run `coverage html` & open `index.html` in browser to drill down to code lines coverage

**Swagger documentation:**

![Swagger documentation](readme_img/swagger_documentation.png)

**Test coverage report obtained via `coverage html`:**

![Test coverage](readme_img/test_coverage_report.png)
