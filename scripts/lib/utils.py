import hashlib
import tempfile
def md5_checksum(file_path):
    """Return the hex MD5 checksum of a local file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def convert_to_s3_key(file_path):
    # Normalize to "folder/file" format, remove SMB share root
    return file_path.replace("\\", "/").lstrip("/")

def verify_upload(bucket, s3_key, local_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        print(f"🔄 Downloading '{s3_key}' from S3 to temporary file...")
        bucket.download_file(s3_key, tmp_file.name)
        downloaded_md5 = md5_checksum(tmp_file.name)
        original_md5 = md5_checksum(local_file)

    print(f"🔎 Local MD5     : {original_md5}")
    print(f"🔎 Downloaded MD5: {downloaded_md5}")
    return downloaded_md5 == original_md5
