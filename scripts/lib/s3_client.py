import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from lib.s3_config import *

def get_s3_resource():
    retry_config = Config(retries={'max_attempts': 5, 'mode': 'standard'})
    return boto3.resource(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION,
        config=retry_config
    )

def ensure_bucket_exists(s3, bucket_name):
    bucket = s3.Bucket(bucket_name)
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        print(f"ℹ️  Bucket '{bucket_name}' already exists.")
    except ClientError:
        s3.create_bucket(Bucket=bucket_name)
        print(f"🪣 Bucket '{bucket_name}' created.")
    return bucket
