#!/bin/sh

# Remove comments and export variables
if [ -f .env ]; then
    export $(cat .env | sed 's/#.*$//' | xargs)
else
    export $(cat .env.example | sed 's/#.*$//' | xargs)
fi
export DATABASE_HOST=carford-db
export DATABASE_USER=tester

sleep 10

if [ ! -d migrations ]; then
    poetry run flask db init
    poetry run flask db migrate
fi

poetry run flask db upgrade

exec poetry run flask run --host=0.0.0.0 --port=5000