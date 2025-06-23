import sys
from lib.env_var import BUCKET_NAME
from lib.s3_client import get_s3_resource, ensure_bucket_exists

def list_bucket_objects(bucket):
    print(f"📂 Listing contents of bucket: {bucket.name}")
    for obj in bucket.objects.all():
        print(f" - {obj.key} ({obj.size} bytes)")

def main():
    try:
        s3 = get_s3_resource()
        print("✅ Connected to S3")

        bucket = ensure_bucket_exists(s3, BUCKET_NAME)

        list_bucket_objects(bucket)

    except Exception as e:
        print("❌ Failed to list contents:")
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
