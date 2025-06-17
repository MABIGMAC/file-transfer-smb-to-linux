import os
from lib.env_var import *
from lib.utils import md5_checksum
from lib.s3_client import get_s3_resource, ensure_bucket_exists, list_bucket_objects

# === Write test file ===
os.makedirs(os.path.dirname(LOCAL_FILE_PATH), exist_ok=True)
with open(LOCAL_FILE_PATH, 'w') as f:
    f.write('Hello from Python!')

# Connect to S3
s3 = get_s3_resource()
print("✅ Connected to S3")

# Ensure bucket exists
bucket = ensure_bucket_exists(s3, BUCKET_NAME)

# Upload file
bucket.upload_file(LOCAL_FILE_PATH, S3_KEY)
print(f"📤 Uploaded '{LOCAL_FILE_PATH}' to '{S3_KEY}'")

# Verify with checksum
local_md5 = md5_checksum(LOCAL_FILE_PATH)
etag = s3.Object(BUCKET_NAME, S3_KEY).e_tag.strip('"')

print(f"🔎 Local MD5: {local_md5}")
print(f"🔎 S3 ETag : {etag}")

if local_md5 == etag:
    print("✅ File upload verified successfully!")
else:
    print("❌ Upload verification failed (checksum mismatch)")

# List contents

list_bucket_objects(bucket)
