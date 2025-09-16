#!/usr/bin/env bash
# Simple backup script: dumps Postgres DB and archives MEDIA
set -euo pipefail
TIMESTAMP=$(date +%F_%H%M)
BACKUP_DIR="backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# Adjust these variables if your docker-compose service names or env differ
DB_SERVICE_NAME="db"
DB_NAME="${POSTGRES_DB:-jerv}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_DUMP_FILE="$BACKUP_DIR/db_$TIMESTAMP.dump"

# Dump database (container must be running)
docker-compose exec -T "$DB_SERVICE_NAME" pg_dump -U "$DB_USER" -F c -d "$DB_NAME" > "$DB_DUMP_FILE"

# Archive media folder
MEDIA_DIR="media"
if [ -d "$MEDIA_DIR" ]; then
  tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" "$MEDIA_DIR"
fi

# Rotate: keep last 14 backups
ls -1dt backups/* | tail -n +15 | xargs -r rm -rf

echo "Backup completed: $BACKUP_DIR"
