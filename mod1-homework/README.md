# Homework 1: Docker, SQL and Terraform for

## Overview

In this homework assignment, we will ingest Green Taxi data into a PostgreSQL database using Python, Pandas, and SQLAlchemy. The provided script downloads data, processes it, and executes SQL queries to analyze the data.

## Project Structure

- `ingest_data.py`: The main script for extracting, loading, and processing the Green Taxi data.
- `docker-compose.yml`: Configuration file for setting up the PostgreSQL database.
- `README.md`: Instructions and details about the homework.

## Instructions

### Environment Setup

1. **Run the Database**  
   Start the PostgreSQL database by running:

   ```bash
   docker-compose up -d
   ```


## Running the Script
 Once the database is running, execute the following command in your terminal to run the data ingestion script:

   ```bash
   python ingest_data.py --pg-user=root --pg-pass=root --pg-host=localhost --pg-port=5432 --pg-db=green_taxi --year 2025 --month 11 --chunksize 1000
   ```

## SQL Queries
 The script includes several SQL queries to analyze the ingested data. Here are a few:

1. For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile ?

    ```bash
    SELECT COUNT(1) 
    FROM green_taxi 
    WHERE trip_distance <= 1 AND lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01';
    ```

2. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.

    ```bash
    SELECT lpep_pickup_datetime, trip_distance 
    FROM green_taxi 
    WHERE trip_distance <= 100 
    ORDER BY trip_distance DESC 
    LIMIT 1;
    ```


4. Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

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


6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

  ```bash
  WITH pu_largest_tip AS (
    SELECT MAX(gt.tip_amount) AS largest_tip_amount
    FROM green_taxi AS gt
    INNER JOIN zones AS z
    ON gt."PULocationID" = z."LocationID"
    WHERE z."Zone" = 'East Harlem North'
    AND TO_CHAR(gt."lpep_pickup_datetime", 'YYYY-MM') = '2025-11'
  )
  SELECT 
      z."Zone" AS DO_Zone,
      gt.tip_amount
  FROM green_taxi gt
  INNER JOIN zones z
  ON gt."DOLocationID" = z."LocationID"
  INNER JOIN pu_largest_tip lt
  ON lt.largest_tip_amount = gt.tip_amount;
 ```




