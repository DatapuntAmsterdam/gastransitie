#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie -f ${DIR}/docker-compose.yml $*
}

#trap 'dc kill ; dc rm -f' EXIT

# For database backups:
rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups
mkdir -p ${DIR}/import_cache

dc build

dc up -d database
dc run importer /deploy/docker-wait.sh

echo "Downloading raw datafiles from object store"
dc run --rm importer python manage.py download_data

echo "Importing data into database"
dc run --rm importer python manage.py run_import
dc run --rm importer python manage.py fix_tables

echo "Running backups"
dc exec -T database backup-db.sh gastransitie

echo "Cleanup import cache"
rm -rf ${DIR}/import_cache

echo "Done"
