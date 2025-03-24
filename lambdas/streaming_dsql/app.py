import json
import os
import psycopg2
import boto3
import schema
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.streaming.s3_object import S3Object
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError, envelopes

logger = Logger()

region = os.environ["REGION"]
cluster_endpoint = os.environ["DSQL_CLUSTER_ENDPOINT"]
data_bucket = os.environ["DATA_BUCKET"]

def generate_token(cluster_endpoint, region):
    client = boto3.client("dsql", region_name=region)
    token = client.generate_db_connect_admin_auth_token(cluster_endpoint, region)
    return token

def get_connection(cluster_endpoint):
    conn = psycopg2.connect(dbname = "postgres",
                        user = "admin", 
                        host= cluster_endpoint,
                        password = generate_token(cluster_endpoint, region),
                        port = 5432,
                        sslmode= 'require',
                        connect_timeout=3)
    return conn

def insert_data(key: str):

    conn = get_connection(cluster_endpoint)
    cursor = conn.cursor()

    query = """
            CREATE TABLE IF NOT EXISTS streaming_table( 
                index int,
                customer_id text,
                first_name text,
                last_name text,
                company text,
                city text,
                country text,
                phone1 text,
                phone2 text,
                email text,
                subscription_date text,
                website text);
        """
    cursor.execute(query)
    conn.commit()

    query = """
        INSERT INTO test_table VALUES (%(index)s, %(customer_id)s, %(first_name)s, %(last_name)s, 
            %(company)s, %(city)s, %(country)s, %(phone1)s, %(phone2)s, %(email)s, 
            %(subscription_date)s, %(website)s)
        ;
        """

    s3 = S3Object(bucket=data_bucket, key=key, is_csv=True)

    for line in s3:
        try:
            validate(event=line, schema=schema.INPUT)
            logger.info(line)
            cursor.execute(query, line)
        except SchemaValidationError as exception:
            logger.exception(f"Data validation Failed. {exception}")
            conn.close()
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Error en la validación de datos",
                }),
            }
        

    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cursor.close()
    # Close connection
    conn.close()
    logger.info("Registros insertados en la base de datos")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Registros insertados en la base de datos",
        }),
    }

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    insert_data(event["detail"]["object"]["key"])
