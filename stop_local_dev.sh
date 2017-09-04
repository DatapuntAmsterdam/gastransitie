#!/bin/bash

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastransitie_dev -f ${DIR}/docker-compose.yml $*;
}

dc down
