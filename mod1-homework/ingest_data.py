import click #used to create command line options for the script
import pandas as pd
from tqdm import tqdm #used for progress bar when ingesting the data into db in batches
from sqlalchemy import create_engine #used to ingest data from dataframe to db


#engine = None

def extract_green_taxi(year, month):
    green_taxi_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    green_taxi_url=f'{green_taxi_prefix}/green_tripdata_{year}-{month:02d}.parquet'
    gt_df = pd.read_parquet(green_taxi_url)
    return gt_df


def extract_zones():
    zones_prefix='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    zones_url=f'{zones_prefix}/taxi_zone_lookup.csv'
    z_df=pd.read_csv(zones_url)
    return z_df

def load_data(engine, year, month, chunk_size):

    gt_df = extract_green_taxi(year, month)
    gt_df.head(0).to_sql(name='green_taxi', con=engine, if_exists='replace') #.head(0) to install just the schema to db without any data yet


    #To add ingest the data in chunks for parquet format
    for i in tqdm(range(0, len(gt_df), chunk_size)):
        gt_df_chunk = gt_df.iloc[i:i + chunk_size]
        gt_df_chunk.to_sql(name='green_taxi', con=engine, if_exists='append', index=False)

    z_df = extract_zones()
    z_df.head(0).to_sql(name='zones', con=engine, if_exists='replace') #.head(0) to install just the schema to db without any data yet

    #To add ingest the data in chunks for parquet format
    for i in tqdm(range(0, len(z_df), chunk_size)):
        z_df_chunk = z_df.iloc[i:i + chunk_size]
        z_df_chunk.to_sql(name='zones', con=engine, if_exists='append', index=False)

def run_queries(engine):
    #Question 3
    df_result= pd.read_sql("SELECT COUNT(1) FROM green_taxi WHERE trip_distance <=1 AND lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'", con=engine)
    print("Question 3 Result:", df_result)

    #Question 4
    df_result1=pd.read_sql("SELECT lpep_pickup_datetime, trip_distance FROM green_taxi WHERE trip_distance <= 100 ORDER BY trip_distance DESC LIMIT 1", con=engine)
    print("Question 4 Result:", df_result1)

    #Question 5
    df_result2 = pd.read_sql('SELECT z."Zone", SUM(gt.total_amount) FROM green_taxi AS gt INNER JOIN zones AS z ON CAST(gt."PULocationID" AS BIGINT) = z."LocationID" WHERE DATE(gt.lpep_pickup_datetime)=\'2025-11-18\' GROUP BY z."Zone" ORDER BY SUM(gt.total_amount) DESC Limit 1', con=engine)
    print("Question 5 Result:", df_result2)
    
    #Question 6
    query="""
    WITH pu_largest_tip AS (
        SELECT MAX(gt.tip_amount) AS largest_tip_amount
        FROM green_taxi AS gt
        INNER JOIN zones AS z
        ON gt."PULocationID"=z."LocationID"
        WHERE z."Zone"=\'East Harlem North\'
        AND TO_CHAR(gt."lpep_pickup_datetime", \'YYYY-MM\') = \'2025-11\'
    )

    SELECT 
        z."Zone" AS DO_Zone,
        gt.tip_amount
    FROM green_taxi gt
    INNER JOIN zones z
    ON gt."DOLocationID" = z."LocationID"
    INNER JOIN pu_largest_tip lt
    ON lt.largest_tip_amount = gt.tip_amount

    """
    df_result3 = pd.read_sql(query, con=engine)
    print("Question 6 Result:", df_result3)

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='green_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--chunksize', default=1000, type=int, help='Chunk size for reading CSV')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize):
    #engine = create_engine('postgresql://root:root@localhost:5432/green_taxi') 
    
    #create database connection
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    load_data(engine, year, month, chunksize)
    run_queries(engine)

if __name__ == '__main__':
    main()