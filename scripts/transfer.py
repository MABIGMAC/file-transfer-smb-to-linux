import os
from smb.SMBConnection import SMBConnection
from smb.base import SharedFile

# === Configuration ===
SMB_SERVER_IP = '192.168.1.100'
SMB_SERVER_NAME = 'WINDOWS-PC'  # NetBIOS name
SMB_SHARE_NAME = 'sharedfolder'
SMB_USERNAME = 'username'
SMB_PASSWORD = 'password'
SMB_DOMAIN = ''  # Often blank
LOCAL_DESTINATION = '/app/data'

print("Starting SMB file transfer...")

try:
    os.makedirs(LOCAL_DESTINATION, exist_ok=True)
    test_file_path = os.path.join(LOCAL_DESTINATION, 'write_test.txt')
    with open(test_file_path, 'w') as f:
        f.write("Write test succeeded.\n")
    print(f"Write test passed: {test_file_path}")
except Exception as e:
    print(f"Write test failed: {e}")
    exit(1)


# === Connect to SMB ===
conn = SMBConnection(
    SMB_USERNAME, SMB_PASSWORD,
    'linux-client', SMB_SERVER_NAME,
    domain=SMB_DOMAIN,
    use_ntlm_v2=True,
    is_direct_tcp=True
)

assert conn.connect(SMB_SERVER_IP, 445), "Connection failed"

# === Transfer Files ===
def transfer_folder(remote_path='', local_path=''):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    files = conn.listPath(SMB_SHARE_NAME, remote_path or '/')
    for f in files:
        if f.filename in ('.', '..'):
            continue
        
        remote_file_path = os.path.join(remote_path, f.filename).replace('\\', '/')
        local_file_path = os.path.join(local_path, f.filename)

        if f.isDirectory:
            transfer_folder(remote_file_path, local_file_path)
        else:
            with open(local_file_path, 'wb') as fp:
                conn.retrieveFile(SMB_SHARE_NAME, remote_file_path, fp)
            print(f"Downloaded: {remote_file_path} -> {local_file_path}")

# === Run Transfer ===
transfer_folder('', LOCAL_DESTINATION)

# === Close Connection ===
conn.close()
