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

# For datafile cache:
docker volume rm -f gastransitie_import_cache
docker volume create --name=gastransitie_import_cache

dc build
dc up -d database

echo "Downloading raw datafiles from object store"
dc run --rm importer ls -la /
dc run --rm importer python manage.py download_data

echo "Importing data into database"
dc run --rm importer python manage.py run_import
dc run --rm importer python manage.py fix_tables

echo "What is running?"
dc ps

echo "Dumping database"
dc run --rm database bash /backup-gastransitie-db.sh
