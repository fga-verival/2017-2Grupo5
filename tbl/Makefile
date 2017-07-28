run:
	# Run the development server
	python3 manage.py runserver_plus 0.0.0.0:8080

migrations:
	# Create all migrations from models
	python3 manage.py makemigrations

migrate:
	# Migrate all migrations on database
	python3 manage.py migrate

superuser:
	# Create a super user on system.
	python3 manage.py createsuperuser

shell:
	# Run iteractive shell of project.
	python manage.py shell_plus

notebook:
	# Run iteractive shell notebook of project
	python manage.py shell_plus --notebook

test:
	# Stop execution of tests when the second test fail
	pytest --maxfail=2

coverage:
	# Run coverage on terminal
	pytest --cov=.

sendcoverage:
	# Run coverage to XML file
	# export CODACY_PROJECT_TOKEN=<PROJECT API TOKEN>
	pytest --cov-report xml --cov=.
	python-codacy-coverage -r coverage.xml
