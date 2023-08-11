.PHONY: test migrate makemigrations run

test:
	python manage.py test

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser