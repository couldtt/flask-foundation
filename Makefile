init:
	pip3 install virtualenv
	virtualenv --python=python3 env/ && source env/bin/activate && pip3 install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

celery:
	python run_celery.py -A app.tasks worker

assets:
	cd app/static && bower install && cd ..

server:
	python manage.py runserver --host 0.0.0.0

db:
	python manage.py recreate_db
