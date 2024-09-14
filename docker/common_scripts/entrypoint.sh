#!/usr/bin/env sh

set -o errexit
set -o nounset

postgres_ready () {
  dockerize -wait "tcp://${POSTGRES_HOST:-parser_db}:${POSTGRES_PORT:-5432}" -timeout 10s
}


until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done
>&2 echo 'Postgres is up - continuing...'

# >&2 echo 'Running migrations'
# (alembic upgrade head)
