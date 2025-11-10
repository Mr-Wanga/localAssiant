#!/bin/bash
set -e

# ================================
# Configurable variables
# ================================
NETWORKS=(
  "localAssiant"
)
VOLUMES=(
  "localAssiant_weaviate:/data/localAssiant/weaviate",
  "localAssiant_share_data:/data/share_data"
)

# =======================================
# Choose environment (.env.dev by default)
# =======================================
ENV_FILE=".env.dev"
if [[ "$1" == "prod" || "$1" == "production" ]]; then
  ENV_FILE=".env.prod"
  echo "🚀 Using production environment: $ENV_FILE"
else
  echo "🧪 Using development environment: $ENV_FILE"
fi

# ================================
# Check and create Docker networks
# ================================
echo
echo "🔍 Checking Docker networks..."
for NET in "${NETWORKS[@]}"; do
  if ! docker network inspect "$NET" >/dev/null 2>&1; then
    echo "⚙️  Creating network: $NET"
    docker network create "$NET"
  else
    echo "✅ Network already exists: $NET"
  fi
done

# ================================
# Check and create Docker volumes
# ================================
echo
echo "🔍 Checking Docker volumes..."
for ITEM in "${VOLUMES[@]}"; do
  VOLUME_NAME="${ITEM%%:*}"
  VOLUME_PATH="${ITEM#*:}"

  if ! docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
    echo "⚙️  Creating volume: $VOLUME_NAME → $VOLUME_PATH"
    mkdir -p "$VOLUME_PATH"
    docker volume create \
      --driver local \
      --opt type=none \
      --opt device="$VOLUME_PATH" \
      --opt o=bind \
      "$VOLUME_NAME"
  else
    echo "✅ Volume already exists: $VOLUME_NAME"
  fi
done

# ================================
# Run docker compose
# ================================
echo
echo "🚀 Starting Docker Compose with ${ENV_FILE}..."
docker compose --env-file "$ENV_FILE" up --build -d

echo
echo "🎉 All services are up!"
docker compose ps

