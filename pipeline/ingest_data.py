#!/usr/bin/env python
# coding: utf-8

import click
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

def load_data_to_sql(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    # PostgreSQL database credentials
    # Parameters for data downloads

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    # Define the columns to parse as dates
    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]
        
    # Create PostgreSQL engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Create the table in PostgreSQL with an empty DataFrame for the schema
    columns = list(dtype.keys()) + parse_dates
    pd.DataFrame(columns=columns).to_sql(name=target_table, con=engine, if_exists='replace', index=False)

    # Read the CSV file into a DataFrame, iterating in chunks
    df_iter = pd.read_csv(
        prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    # Process each chunk of data and write to SQL
    for df_chunk in tqdm(df_iter, desc="Processing chunks"):
        print(f"Processing chunk: {df_chunk.shape}")
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append', index=False)

    print("Data loading complete!")

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='172.17.0.2', help='Database host')
@click.option('--pg-port', default='5432', help='Database port')
@click.option('--pg-db', default='ny_taxi', help='Database name')
@click.option('--year', default=2021, type=int, help='Year for data')
@click.option('--month', default=1, type=int, help='Month for data')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for processing')
def main(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, table, chunksize):
    load_data_to_sql(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, table, chunksize)

if __name__ == "__main__":
    main()
