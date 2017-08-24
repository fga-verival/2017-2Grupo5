# INSTALL --------------------------------------
install:
	# Create tbl enviroment
	# BUG: Not work yet
	mkvirtualenv tbl
	pip3 install -r requeriments-dev.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
	django-admin makemessages
	django-admin compilemessages

dev:
	# Get in on dev enviroment
	workon dev

clean:
	# Search and clean all files .pyc and .pyo in __pycache__ directories
	# Run it before run make test
	find . | grep -E "(\.pyc|\.pyo)" | xargs rm -rf

# SERVER ---------------------------------------
run:
	# Run the development server
	python3 manage.py runserver 0.0.0.0:8080

# DATABASE -------------------------------------

migrations:
	# Create all migrations from models
	python3 manage.py makemigrations

migrate:
	# Migrate all migrations on database
	python3 manage.py migrate

superuser:
	# Create a super user on system.
	python3 manage.py createsuperuser

# SHELL ---------------------------------------

shell:
	# Run iteractive shell of project.
	python3 manage.py shell_plus

notebook:
	# Run iteractive shell notebook of project
	python3 manage.py shell_plus --notebook

# TRANSLATION ---------------------------------

makemessages:
	# Create a django.po to insert translations (pt-BR)
	django-admin makemessages -l pt_BR

compilemessages:
	# Create translations
	django-admin compilemessages

# STATIC FILES --------------------------------

staticfiles:
	# Collect all static files
	python3 manage.py collectstatic

# TESTS ---------------------------------------

test:
	# Stop execution of tests when the second test fail
	# Run make clean before it
	pytest --maxfail=1

coverage:
	# Run coverage on terminal
	pytest --maxfail=1 --cov=.

sendcoverage:
	# Run coverage to XML file
	# export CODACY_PROJECT_TOKEN=<PROJECT API TOKEN>
	pytest --cov-report xml --cov=.
	python-codacy-coverage -r coverage.xml
