
# Developer Guide

Install the dependencies:

```bash
poetry install
```

Set up a development Postgres database. Refer to `language_listening_practice_app/settings.py` for the database configuration.

Run the tests:

```bash
make test
```

Or

```bash
make testdev
```

To run the tests in watch mode (re-runs tests on file changes).

Run migrations:

```bash
make migrate
```

Run the dev server:

```bash
make dev
```

