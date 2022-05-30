FROM ubuntu:18.04

MAINTAINER Emilio  "emilio.cimino@outlook.it"

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN apt-get install -y ffmpeg


COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN useradd app


COPY license.txt speechtotext.proto speechtotext_pb2.py speechtotext_pb2_grpc.py Converter.py ./app/
WORKDIR /app/
RUN chown -R app:app /app
RUN chmod 755 /app

USER app

ENTRYPOINT [ "python3","Converter.py" ]
