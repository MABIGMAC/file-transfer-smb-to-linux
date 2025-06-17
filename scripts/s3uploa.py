import boto3
import hashlib
import os
from botocore.exceptions import ClientError
from datetime import timezone

# Configuration
S3_ENDPOINT = 'http://localhost:9000'  # or 'http://minio:9000' in Docker
AWS_ACCESS_KEY = 'minioadmin'
AWS_SECRET_KEY = 'minioadmin123'
REGION = 'us-east-1'
BUCKET_NAME = 'my-test-bucket'
LOCAL_FILE_PATH = 'data/test.txt'
S3_KEY = 'uploaded/test.txt'

def list_bucket_objects(bucket_name):
    print(f"\n📂 Contents of bucket '{bucket_name}':")
    bucket = s3.Bucket(bucket_name)
    found = False
    for obj in bucket.objects.all():
        uploaded_at = obj.last_modified.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f" - {obj.key} ({obj.size} bytes) | Uploaded at: {uploaded_at}")
        found = True
    if not found:
        print(" - (empty)")

# === Helpers ===
def md5_checksum(file_path):
    """Return the hex MD5 checksum of a local file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# === Write test file ===
os.makedirs(os.path.dirname(LOCAL_FILE_PATH), exist_ok=True)
with open(LOCAL_FILE_PATH, 'w') as f:
    f.write('Hello from Python!')

# Connect to S3 (MinIO)
s3 = boto3.resource(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

print("✅ Connected to S3")

# Create the bucket if it doesn't exist
bucket = s3.Bucket(BUCKET_NAME)
try:
    s3.meta.client.head_bucket(Bucket=BUCKET_NAME)
    print(f"ℹ️  Bucket '{BUCKET_NAME}' already exists.")
except ClientError:
    s3.create_bucket(Bucket=BUCKET_NAME)
    print(f"🪣 Bucket '{BUCKET_NAME}' created.")

# Upload a file
bucket.upload_file(LOCAL_FILE_PATH, S3_KEY)
print(f"📤 Uploaded '{LOCAL_FILE_PATH}' to '{S3_KEY}'")

# === Verify with checksum ===
local_md5 = md5_checksum(LOCAL_FILE_PATH)
obj = s3.Object(BUCKET_NAME, S3_KEY)
etag = obj.e_tag.strip('"')

print(f"🔎 Local MD5: {local_md5}")
print(f"🔎 S3 ETag : {etag}")

if local_md5 == etag:
    print("✅ File upload verified successfully!")
else:
    print("❌ Upload verification failed (checksum mismatch)")

list_bucket_objects(BUCKET_NAME)