import boto3
from botocore.exceptions import ClientError, BotoCoreError
from botocore.config import Config
from lib.env_var import *
from datetime import timezone


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

# Check if file already exists in S3
def file_exists_in_s3(s3_client, s3_bucket, file_key):
    # Use s3_client.head_object() or list_objects_v2()
    # Return True if exists, False otherwise
    pass

def list_bucket_objects(bucket):
    print(f"\n📂 Contents of bucket '{bucket.name}':")
    found = False
    for obj in bucket.objects.all():
        uploaded_at = obj.last_modified.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f" - {obj.key} ({obj.size} bytes) | Uploaded at: {uploaded_at}")
        found = True
    if not found:
        print(" - (empty)")

def upload_file_with_validation(bucket, local_path, s3_key):
    try:
        print(f"🔄 Uploading '{local_path}' to S3 bucket '{bucket.name}' as '{s3_key}'...")
        bucket.upload_file(local_path, s3_key)
        print(f"📤 Uploaded '{local_path}' to '{s3_key}'")
    except (BotoCoreError, ClientError) as e:
        print(f"❌ Upload failed: {e}")
        # Check if the file partially exists in S3
        try:
            bucket.Object(s3_key).load()
            print("⚠️ File partially or unexpectedly exists in S3.")
        except ClientError as err:
            if err.response['Error']['Code'] == '404':
                print("✅ No file found in S3 after failed upload.")
            else:
                print(f"⚠️ Unexpected error when checking S3: {err}")