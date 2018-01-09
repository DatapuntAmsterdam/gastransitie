#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

# For database backups:
rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

echo "For debugging list volumes"
dc down	-v
docker volume ls

echo "Building images"
dc build

echo "Bringing up and waiting for database"
dc up -d database
dc run importer /deploy/docker-wait.sh

echo "Downloading raw datafiles from object store"
dc run --rm importer ls /data
dc run --rm importer python manage.py download_data

echo "Importing data into database"
dc run --rm importer python manage.py run_import
dc run --rm importer python manage.py fix_tables

echo "Running backups"
dc exec -T database backup-db.sh gastransitie

echo "Remove containers and volumes."
dc down -v
dc rm -f

echo "Done"
