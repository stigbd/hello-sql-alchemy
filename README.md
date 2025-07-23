# hello-sql-alchemy

This is a simple project to demonstrate how to use [SQLAlchemy](https://www.sqlalchemy.org/) and [Alembic](https://alembic.sqlalchemy.org/) with [Pydantic](https://docs.pydantic.dev/) in Python. It uses [SQLite](https://www.sqlite.org/) as the database and provides a basic example of how to create a table, insert data, and query it.


To run it, you need to install the dependencies. Using [uv](https://docs.astral.sh/uv/), you can do this easily:

```bash
uv sync
```

Also you will have to create a `.env` file in the root directory of the project with the following content:

```env
DATABASE_URL=sqlite:///./test.db
```

Then, you can run the example script:

```bash
uv run hello-sql-alchemy
```

## Database migration

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
uv run alembic upgrade head
```
