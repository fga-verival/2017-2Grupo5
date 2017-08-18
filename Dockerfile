# Build an debian image
FROM debian:8.7

# Set the working directory to /software
ADD . /software
WORKDIR /software

# Update, Upgrade and configure locale
RUN apt-get update

# Install dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    git-core \
    openssl \
    build-essential \
    nginx

RUN pip3 install --upgrade pip
RUN pip3 install -r tbl/requirements.txt
RUN python3 tbl/manage.py makemigrations
RUN python3 tbl/manage.py migrate
RUN django-admin compilemessages
