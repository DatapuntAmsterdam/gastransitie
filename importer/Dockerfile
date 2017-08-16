FROM amsterdam/docker_python:latest

COPY importer /app/
RUN mkdir /data
COPY .jenkins-import /.jenkins-import/

ADD /import.sh /app/import.sh
ENTRYPOINT /app/import.sh

