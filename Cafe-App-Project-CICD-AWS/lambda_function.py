# from extract import *
# from load_drop_dupe_db import load_data
# from table_script import create_table
from app import run_etl_main
import pandas as pd
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context=None):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        fieldnames = ['timestamp', 'store', 'customer_name',
                      'basket_items', 'total_price', 'cash_or_card', 'card_number']
        df = pd.read_csv(response["Body"], names=fieldnames)
        run_etl_main(df)
        print('All completed')
    except Exception as e:
        print(e)
        print(
            f"Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same region as this function.")
        raise e
    print(key)
