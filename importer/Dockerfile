FROM amsterdam/docker_python:latest

COPY importer /app/
RUN mkdir /data
COPY .jenkins-import /.jenkins-import/

ADD /import.sh /app/import.sh
ADD /docker-wait.sh /app/docker-wait.sh
ADD /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
CMD /app/import.sh

