FROM debian:8.7

RUN apt-get update
RUN apt-get -y upgrade
RUN locale-gen en_GB.UTF-8
RUN locale-gen pt_BR.UTF-8
RUN apt-get install -y python3-dev \
    sqlite \
    python3-pip

RUN pip3 install --upgrade pip
#RUN pip3 install -r requirements-deploy.txt
