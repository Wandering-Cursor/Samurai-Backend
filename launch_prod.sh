docker build -t samurai-backend-web .
docker compose -f ./compose/prod-docker-compose.yml up -d
