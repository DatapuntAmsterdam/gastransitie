#!/bin/sh

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

dc build
dc run --rm importer
dc exec -T database update-table.sh bag bag_buurt public gastransitie
dc exec -T database update-table.sh bag bag_verblijfsobject public gastransitie
# following commands need the tables above to exist to work:
dc run --rm importer bash /app/run_add_views.sh
dc run --rm importer bash /app/run_additional_sql.sh

# dump the database
dc run --rm db-backup
