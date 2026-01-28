### Homework: ELT Datapipeline Homework

## Overview 

In this homework assignment, we will create a datapipeline with the use of kestra for orchestration and load the data to GCP. 

## Project Structure 
<img width="1032" height="196" alt="image" src="https://github.com/user-attachments/assets/a2927a35-d30c-44b7-92cd-0c5705aa3e3c" />

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
The script includes several SQL queries to analyze the ingested data. Here are a few: 

1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)? 

```bash
   - id: log_file_size
    type: io.kestra.plugin.core.log.Log
    message: "The uncompressed file size is: {{ fileSize(outputs.extract.outputFiles[render(vars.file)]) }} bytes"
 ```
<img width="693" height="176" alt="image" src="https://github.com/user-attachments/assets/5c26cd5c-bd7a-4fec-be27-118c794c2544" />

**Answer**: `134.5 MiB`


2. What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution? 

```bash
{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv
 ```

**Answer**: `green_tripdata_2020-04.csv`

3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

```bash
    SELECT COUNT(*)
    FROM `zoomcamp.yellow_tripdata`
    WHERE filename LIKE 'yellow_tripdata_2020%'
 ```


**Answer**: `24,648,499`
 
4.  How many rows are there for the Green Taxi data for all CSV files in the year 2020?
   
```bash
   SELECT COUNT(*)
   FROM `zoomcamp.green_tripdata`
   WHERE filename LIKE 'green_tripdata_2020%'
 ```

**Answer**: `1,734,051`

5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

```bash
    SELECT COUNT(*)
    FROM `zoomcamp.yellow_tripdata`
    WHERE filename LIKE 'yellow_tripdata_2021_03.csv%'
 ```

**Answer**: `1,925,152`

6. How would you configure the timezone to New York in a Schedule trigger?

```bash
 triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York
    inputs:
      taxi: green

  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    timezone: America/New_York
    inputs:
      taxi: yellow
```
**Answer**: `Add a timezone property set to America/New_York in the Schedule trigger configuration`


## References:

[02-Workflow Orchestration Module](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration)

[Homework Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/02-workflow-orchestration/homework.md)
   





