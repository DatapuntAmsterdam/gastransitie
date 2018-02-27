FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt update \
	&& adduser --system datapunt \
	&& mkdir -p /static \
	&& chown datapunt /static \
	&& mkdir /data \
	&& chown datapunt /data

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

USER datapunt
COPY ./app/ /app/
COPY ./deploy/ /deploy/
