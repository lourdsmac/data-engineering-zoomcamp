### Homework: Ingesting Green Taxi Data 

## Overview 

In this homework assignment, we will ingest Green Taxi data into a PostgreSQL database using Python, Pandas, and SQLAlchemy. The provided script downloads data, processes it, and executes SQL queries to analyze the data. 

## Project Structure 

- ingest_data.py: The main script for extracting, loading, and processing the Green Taxi data.
- docker-compose.yml: Configuration file for setting up the PostgreSQL database.


## Instructions 

### Prerequisites
- Docker and Docker Compose installed
- Terraform

### Environment Setup 

1. Run the Database

   Start the PostgreSQL database by running:

```bash
   docker-compose up -d
```

### Running the Script
 Once the database is running, execute the following command in your terminal to run the data ingestion script:

```bash
python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5431 \
  --pg-db=green_taxi \
  --year 2025 \
  --month 11 \
  --chunksize 1000
 ```

## Homework 
The script includes several SQL queries to analyze the ingested data. Here are a few: 

1. What's the version of pip in the python:3.13 image?
```bash
  docker run -it --entrypoint bash python:3.13
  pip --version
 ```
**Answer**: `25.3`


2. Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

```bash
services:
  db:
    image: postgres:18
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: "green_taxi"
    volumes:
      - green_taxi_postgres_data:/var/lib/postgresql
    ports:
      - "5431:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: "admin@admin.com"
      PGADMIN_DEFAULT_PASSWORD: "root"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    ports:
      - "8085:80"

volumes:
  green_taxi_postgres_data:
  pgadmin_data:
 ```

**Answer**: `db:5432`

**Explanation**:  pgAdmin should use hostname "db" because the service name in your docker-compose.yml becomes the container’s internal network hostname that other containers use, and it should use port 5432 because that is PostgreSQL’s default port which the Postgres server inside the container listens on.



3. For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile ?

```bash
    SELECT COUNT(1) 
    FROM green_taxi 
    WHERE trip_distance <= 1 AND lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01';
 ```

**Answer**: `8,007`
 
4. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.
```bash
 SELECT lpep_pickup_datetime, trip_distance FROM green_taxi WHERE trip_distance <= 100 ORDER BY trip_distance DESC LIMIT 1;
 ```

**Answer**: `2025-11-14`

5. Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```bash

    SELECT z."Zone", SUM(gt.total_amount) 
    FROM green_taxi AS gt 
    INNER JOIN zones AS z 
    ON CAST(gt."PULocationID" AS BIGINT) = z."LocationID" 
    WHERE DATE(gt.lpep_pickup_datetime) = '2025-11-18' 
    GROUP BY z."Zone" 
    ORDER BY SUM(gt.total_amount) DESC 
    LIMIT 1;
 ```
**Answer**: `East Harlem North`

6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

```bash
WITH pu_largest_tip AS (
  SELECT
    MAX(gt.tip_amount) AS largest_tip_amount
  FROM
    green_taxi AS gt
    INNER JOIN zones AS z
      ON gt."PULocationID" = z."LocationID"
  WHERE
    z."Zone" = 'East Harlem North'
    AND TO_CHAR(gt."lpep_pickup_datetime", 'YYYY-MM') = '2025-11'
)
SELECT
  z."Zone" AS DO_Zone,
  gt.tip_amount
FROM
  green_taxi gt
  INNER JOIN zones z
    ON gt."DOLocationID" = z."LocationID"
  INNER JOIN pu_largest_tip lt
    ON lt.largest_tip_amount = gt.tip_amount;

```
**Answer**: `Yorkville West`

7. Which of the following sequences describes the Terraform workflow for: 1) Downloading plugins and setting up backend, 2) Generating and executing changes, 3) Removing all resources?
**Answer**: `terraform init, terraform apply -auto-approve, terraform destroy`

**Explanation:**

`terraform init`: 

Purpose: Prepares your environment.

Actions: Downloads necessary plugins and sets up the backend for storing your Terraform state.

`terraform apply -auto-approve`:

Purpose: Creates or updates infrastructure based on your configuration.

Actions: Automatically applies changes without asking for confirmation.

`terraform destroy`:

Purpose: Cleans up everything.

Actions: Completely removes all resources that were created.
   
