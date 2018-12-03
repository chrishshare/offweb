FROM python:3.6.4
ENV PYTHONUMBUFFERED 1
RUN mkdir /offweb
RUN mkdir /offweb/dockermysql
WORKDIR /offweb
ADD requirements.txt /offweb/
RUN pip install -r requirements.txt
ADD . /offweb/
