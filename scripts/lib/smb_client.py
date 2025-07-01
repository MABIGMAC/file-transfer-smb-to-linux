from smbclient import (
    register_session, open_file, remove, rename,
    stat, symlink, link, listdir
)
from lib.env_var import *
import os

# Register session once
register_session(SMB_SERVER, username=SMB_USER, password=SMB_PASS, port=SMB_PORT)

# Build base UNC path
base_path = fr"\\{SMB_SERVER}\{SMB_SHARE}".rstrip("\\")

def list_smb_files_recursive(path: str) -> list[str]:
    """Recursively list all files under the given SMB path."""
    files = []
    try:
        for entry in listdir(path):
            full_path = os.path.join(path, entry)

            try:
                info = stat(full_path)
                if info.st_mode & 0o170000 == 0o040000:  # Directory
                    files.extend(list_smb_files_recursive(full_path))
                else:
                    files.append(full_path)
            except Exception as e:
                print(f"Failed to stat {full_path}: {e}")
    except Exception as e:
        print(f"Failed to list {path}: {e}")

    return files


def list_smb_files() -> list[str]:
    """Return all file paths under the base SMB share."""
    return list_smb_files_recursive(base_path)