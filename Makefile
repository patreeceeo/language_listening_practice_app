
dev:
	python manage.py runserver

migrate:
	python manage.py migrate

tests:
	python manage.py test

testdev:
	find . -name '*.py' | entr python manage.py test
