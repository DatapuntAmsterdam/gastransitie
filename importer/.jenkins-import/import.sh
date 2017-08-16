#!/bin/bash

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p hr -f ${DIR}/docker-compose.yml $*;
}

dc pull

trap 'dc kill ; dc rm -f -v' EXIT

echo "Do we have OS password?"
echo $GASTRANSITIE_OBJECTSTORE_PASSWORD
echo "Do we have ENVIRONMENT?"
echo $ENVIRONMENT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc build --pull

dc up -d database

# wait to give postgres the change to be up
sleep 50

# load latest bag into database
echo "Load latest verblijfsobjecten en nummeraanduidingen in gastransitie database"

# dc exec -T database update-db.sh atlas
dc exec -T database update-table.sh bag bag_buurt public gastransitie
# dc exec -T database update-table.sh bag bag_nummeraanduiding public gastransitie

echo "create gastransitie api database"
dc run --rm importer

echo "DONE! importing mks into database"

echo "create gastransitie dump"
# run the backup shizzle
dc run --rm db-backup

echo "DONE! with Import! You are awesome! <3"
