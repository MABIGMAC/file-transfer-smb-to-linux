import os
import time
from lib.env_var import *
from lib.utils import verify_upload, md5_checksum, calculate_s3_multipart_etag
from lib.s3_client import get_s3_resource, ensure_bucket_exists, list_bucket_objects, upload_file_with_validation, put_object_with_validation

# # === Write test file ===
# os.makedirs(os.path.dirname(LOCAL_FILE_PATH), exist_ok=True)
# with open(LOCAL_FILE_PATH, 'w') as f:
#     f.write('Hello from Python!')

# Connect to S3
s3 = get_s3_resource()
print("✅ Connected to S3")

# Ensure bucket exists
bucket = ensure_bucket_exists(s3, BUCKET_NAME)

# Upload file
upload_file_with_validation(bucket, LOCAL_FILE_PATH, S3_KEY)
# put_object_with_validation(bucket, LOCAL_FILE_PATH, S3_KEY)

# # Verify with checksum
start_time = time.time()  # ⏱️ Start timer


locallasttag = calculate_s3_multipart_etag(LOCAL_FILE_PATH)
etag = s3.Object(BUCKET_NAME, S3_KEY).e_tag.strip('"')
print(f"🔎 Local ETag: {locallasttag}")
print(f"🔎 S3 ETag : {etag}")
# verifyed = verify_upload(bucket, S3_KEY, LOCAL_FILE_PATH)

if locallasttag == etag:
    print("✅ File upload verified successfully!")
else:
    print("❌ Upload verification failed (checksum mismatch)")
end_time = time.time()    # ⏱️ End timer
duration = end_time - start_time
print(f"⏱️ Verification completed in {duration:.2f} seconds")

# List contents

list_bucket_objects(bucket)
