FROM python:3.12-alpine


WORKDIR /base

# Install dependencies
COPY poetry.lock pyproject.toml /base/
RUN pip install poetry && poetry install --no-root

COPY . /base/
COPY entrypoint.sh /base


# Check .env exists, if it doesnt rename .env.example to .env
RUN test -f .env || cp env-example /base/.env

RUN chmod +x /base/entrypoint.sh

EXPOSE 5000
# CMD [ "poetry", "run", "flask", "run",  "--host=0.0.0.0", "--port=5000" ]
ENTRYPOINT [ "/base/entrypoint.sh" ]
