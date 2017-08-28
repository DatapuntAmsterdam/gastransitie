FROM amsterdam/docker_python:latest

#RUN mkdir /app
RUN mkdir /data

ADD /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY importer /app/

ADD /run_import.sh /app/run_import.sh
ADD /run_test.sh /app/run_test.sh
ADD /run_add_views.sh /app/run_add_views.sh
ADD /docker-wait.sh /app/docker-wait.sh

# Do the .jenkins directory dance to enable data imports:
COPY .jenkins/import /.jenkins-import/
COPY .jenkins /app/.jenkins

# run the import (TBD: still relevant?)
CMD /app/run_import.sh

