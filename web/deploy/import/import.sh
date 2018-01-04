#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p onderwijs -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc build
dc up -d database

echo "Downloading raw datafiles from object store"
dc run --rm importer python manage.py download_data

echo "Importing data into database"
dc run --rm importer python manage.py run_import
dc run --rm importer python manage.py fix_tables

echo "Dumping database"
dc run --rm database /backup-gastransitie-db.sh