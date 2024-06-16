FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry install --no-root

COPY . .
COPY .env /app/

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]