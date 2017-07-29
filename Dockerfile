# Build an debian image
FROM debian:8.7

# Update, Upgrade and configure locale
RUN apt-get update
RUN apt-get -y upgrade

# Install dependecies
RUN apt-get install -y python3-dev \
    python3-pip \
    libpq-dev \
    gettext \
    git-core \
    openssl
RUN pip3 install --upgrade pip
RUN git clone https://github.com/TeamBasedLearning/Service.git tbl

# Set the working directory to /tbl
WORKDIR /tbl

RUN pip3 install -r tbl/requirements.txt
RUN python3 tbl/manage.py makemigrations
RUN python3 tbl/manage.py migrate
RUN django-admin makemessages
RUN django-admin compilemessages
