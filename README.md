# hello-sql-alchemy

This is a simple project to demonstrate how to use [SQLAlchemy](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/) with [Pydantic](https://docs.pydantic.dev/) in Python. It uses [PostgreSQL](https://www.postgresql.org/) as the database and provides a basic example of how to create a table, insert data, and query it.


To run it, you need to install the dependencies. Using [uv](https://docs.astral.sh/uv/), you can do this easily:

```bash
uv sync
```

Also you will have to create a `.env` file in the root directory of the project with the following content:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_NAME=test_db
```

Then, you can run the FastAPI application using:

```bash
uv run --env-file=.env fastapi dev
```

Running in docker compose:

```bash
docker compose up -d
docker compose exec api uv run alembic upgrade head
```

## Example usage

Create a new user by sending a POST request to `/users/` with the following JSON body:

```json
{
  "name": "john-doe",
  "fullname": "John Doe"
}
```

You can use `curl` to do this:

```bash
curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d '{"name": "john-doe", "fullname": "John Doe"}'
```

List all users by sending a GET request to `/users/`:

```bash
curl -X GET http://localhost:8000/users
```

Get a specific user by sending a GET request to `/users/{user_id}`:

```bash
curl -X GET http://localhost:8000/users/1
```

## Database migrations

The alembic configuration was set up using:

```bash
uv run alembic init --template pyproject alembic
```

To create the initial migration, you can use:

```bash
uv run alembic revision --autogenerate -m "Initial migration"
```

To run database migrations, do:

```bash
uv run --env-file=.env alembic upgrade head
```
