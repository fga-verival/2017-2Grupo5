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
    openssl \
    build-essential \
    nginx

RUN pip3 install --upgrade pip
RUN git clone https://github.com/TeamBasedLearning/Service.git software

# Set the working directory to /tbl
WORKDIR /software

RUN pip3 install -r tbl/requirements.txt
RUN python3 tbl/manage.py makemigrations
RUN python3 tbl/manage.py migrate
RUN django-admin makemessages
RUN django-admin compilemessages

# Setup nginx to make our application accessible.
RUN cp /software/deploy/nginx_tbl.conf /etc/nginx/sites-available/nginx_tbl.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/nginx_tbl.conf /etc/nginx/sites-enabled/nginx_tbl.conf
systemctl restart nginx.service
