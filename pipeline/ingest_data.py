#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Define data types for specific columns
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

# PostgreSQL database credentials
pg_user = 'root'                    # Your PostgreSQL username
pg_password = 'root'                # Your PostgreSQL password
pg_host = 'localhost'               # Database host (use 'host.docker.internal' if using Docker)
pg_port = '5432'                    # Database port
pg_db = 'ny_taxi'                   # Database name

# Parameters for data downloads
year = 2021
month = 1
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

# Define the columns to parse as dates
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def load_data_to_sql():
    # Create PostgreSQL engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Create the table in PostgreSQL with an empty DataFrame for the schema
    pd.DataFrame(columns=dtype.keys()).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace', index=False)

    # Read the CSV file into a DataFrame, iterating in chunks
    df_iter = pd.read_csv(
        prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )

    # Process each chunk of data and write to SQL
    for df_chunk in tqdm(df_iter, desc="Processing chunks"):
        print(f"Processing chunk: {df_chunk.shape}")
        df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append', index=False)

    print("Data loading complete!")

def main():
    load_data_to_sql()

if __name__ == "__main__":
    main()
