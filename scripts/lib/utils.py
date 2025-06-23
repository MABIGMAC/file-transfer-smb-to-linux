import hashlib
import tempfile
import time

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

import hashlib

def calculate_s3_multipart_etag(file_path, part_size=8 * 1024 * 1024):
    md5s = []
    with open(file_path, 'rb') as f:
        while chunk := f.read(part_size):
            md5s.append(hashlib.md5(chunk).digest())

    if len(md5s) == 1:
        return hashlib.md5(md5s[0]).hexdigest()
    else:
        joined_md5 = b''.join(md5s)
        final_etag = hashlib.md5(joined_md5).hexdigest()
        return f"{final_etag}-{len(md5s)}"


def verify_upload(bucket, s3_key, local_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        print(f"🔄 Downloading '{s3_key}' from S3 to temporary file...")
        start_time = time.time()  # ⏱️ Start timer

        bucket.download_file(s3_key, tmp_file.name)

        end_time = time.time()    # ⏱️ End timer
        duration = end_time - start_time
        print(f"⏱️ Download completed in {duration:.2f} seconds")
        downloaded_md5 = md5_checksum(tmp_file.name)
        original_md5 = md5_checksum(local_file)

    print(f"🔎 Local MD5     : {original_md5}")
    print(f"🔎 Downloaded MD5: {downloaded_md5}")
    return downloaded_md5 == original_md5
