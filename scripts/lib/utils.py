import hashlib

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