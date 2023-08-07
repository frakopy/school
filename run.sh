j2 docker-compose.yml.j2 env_DEV.json > docker-compose.yml
docker-compose build
docker-compose up -d 
