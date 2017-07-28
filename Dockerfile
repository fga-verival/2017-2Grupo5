# Build an debian image
FROM debian:8.7

# Add the current dictory . into the path /tbl in the image
ADD . /tbl

# Set the working directory to /tbl
WORKDIR /tbl

# Update, Upgrade and configure locale
RUN apt-get update
RUN apt-get -y upgrade

# Install dependecies
RUN apt-get install -y python3-dev \
    sqlite \
    python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r tbl/requirements.txt

# Run the server
CMD ["python3", "tbl/manage.py", "runserver", "0.0.0.0:8080"]
