### Homework: Datawarehouse and Big Query

## Overview 

In this homework, we will create a datapipeline and use Bigquery for the data warehouse. 

## Workflow
<img width="195" height="484" alt="image" src="https://github.com/user-attachments/assets/1085e6e2-3976-405e-8f3e-6a662ea0e03f" />


## Instructions 

### Prerequisites
- Docker and Docker Compose installed

### Environment Setup 

1. Run the Database

   Run the Data Pipeline database by exuecuting the following command:

    ```bash
       docker-compose up -d
    ```
    
## Homework 
    
1.  What is count of records for the 2024 Yellow Taxi Data? 
    
    ```bash
    SELECT count(*) FROM `data-warehouse-486704.nytaxi.yellow_taxi`;
     ```
    
    **Answer**: `20,332,093`


2. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table? 

    - External Table
    <img width="723" height="93" alt="image" src="https://github.com/user-attachments/assets/6e2bf924-ed82-4082-a4ec-c4c83b710615" />
    
    
    - Materialized Table
    <img width="538" height="79" alt="image" src="https://github.com/user-attachments/assets/578dbdd9-959e-4e9e-8359-c2180447aa42" />
    
    
    **Answer**: `0 MB for the External Table and 155.12 MB for the Materialized Table`


3. Why are the estimated number of Bytes different?
    
    **Answer**: `BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.`
     
4.  How many records have a fare_amount of 0?
   
    ```bash
    SELECT COUNT(*) FROM `data-warehouse-486704.nytaxi.yellow_tripdata_external` WHERE fare_amount=0;
     ```
    
    **Answer**: `8,333`

5. What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

    ```bash
    CREATE OR REPLACE TABLE `data-warehouse-486704.nytaxi.yellow_tripdata_partitioned_clustered`
    PARTITION BY DATE(tpep_dropoff_datetime)
    CLUSTER BY VendorID AS
    SELECT * FROM data-warehouse-486704.nytaxi.yellow_tripdata_external;
     ```
    
    **Answer**: `Partition by tpep_dropoff_datetime and Cluster on VendorID`

6. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values??
    
    - Materialized Table
    <img width="610" height="94" alt="image" src="https://github.com/user-attachments/assets/b93ffaae-7a5d-45c9-83e7-79a4823402a7" />
    
    - Partitioned and Clustered
    <img width="803" height="93" alt="image" src="https://github.com/user-attachments/assets/aeac2a0d-ab99-481e-a824-c138de910cfb" />


    **Answer**: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

7.  Where is the data stored in the External Table you created?

      **Answer**: `GCP Bucket`
      
      **Explanation:**
      
      An external table in BigQuery:
      
      - does NOT store data inside BigQuery
      
      - only stores metadata (schema + file locations)

      - reads the actual data directly from Google Cloud Storage (GCS)

8. It is best practice in Big Query to always cluster your data:

    **Answer**: `False`
    
    **Explanation:**
    
    Clustering should be applied selectively based on query patterns and data size, not by default, as it can add unnecessary overhead.
    
    When clustering does NOT make sense
    
    - Small datasets
    
    - Ad-hoc queries
    
    - Columns rarely used in filters

## References:

[03-Data Warehouse](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/03-data-warehouse)

[Homework Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/03-data-warehouse/homework.md)

