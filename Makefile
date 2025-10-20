
css-build:
	npm run build:css

css-watch:
	npm run watch:css

dev:
	@echo "Starting CSS watcher and Django server..."
	@trap 'kill 0' EXIT; npm run watch:css & python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

tests:
	python manage.py test

testdev:
	find . -name '*.py' | entr python manage.py test

repl:
	python manage.py shell
