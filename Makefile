runserver:
	python manage.py runserver localhost:8000

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

manage:
	python manage.py ${C}

