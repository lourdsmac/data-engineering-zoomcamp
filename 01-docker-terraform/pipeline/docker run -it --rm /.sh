docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5433:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:18



  docker run -it --rm \
    --network=pg-network \
    taxi_ingest:v001 \
    --pg-user root \
    --pg-password root \
    --pg-host pg-database \
    --pg-port 5432 \
    --pg-db ny_taxi \
    --year 2021 \
    --month 1 \
    --table yellow_taxi_data \
    --chunksize 100000

