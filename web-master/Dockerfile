FROM centos:7
MAINTAINER Youngsun: version 1.1

CMD ["init"]

RUN yum update -y ; yum clean all 

# python 3.6.8
RUN yum install python3 -y ; yum clean all
RUN pip3 install --upgrade setuptools
RUN pip3 install six

# mysql  Ver 15.1 Distrib 5.5.64-MariaDB, for Linux (x86_64) using readline 5.1
RUN yum install mariadb-server -y ; yum clean all
RUN yum install -y mariadb-devel gcc ; yum clean all
RUN yum install -y python3-devel ; yum clean all
RUN pip3 install mysqlclient

# django 3.0.5
RUN pip3 install django

# copy project folder
RUN mkdir /app
COPY ./web-backend /app/
RUN find /app -path '*/__pycache__*' -delete
RUN find /app -path '*/migrations*' -delete