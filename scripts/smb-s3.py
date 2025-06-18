# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

# Worker thread logic
def worker_thread(queue, smb_connection, s3_client, s3_bucket):
    while True:
        try:
            file_path = queue.get(timeout=3)  # Wait for file path or exit
        except Queue.Empty:
            return

        try:
            # Construct S3 key from SMB path
            s3_key = convert_to_s3_key(file_path)

            # Check existence
            if not file_exists_in_s3(s3_client, s3_bucket, s3_key):
                upload_file_to_s3(smb_connection, s3_client, s3_bucket, file_path, s3_key)
                print(f"Uploaded: {file_path}")
            else:
                print(f"Already exists: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        finally:
            queue.task_done()

# Main logic
def main():
    smb_connection = connect_to_smb()
    s3_client = connect_to_s3()
    s3_bucket = "your-bucket-name"

    file_paths = list_all_smb_file_paths(smb_connection)

    queue = Queue()
    for path in file_paths:
        queue.put(path)

    # Start 10 threads
    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker_thread, args=(queue, smb_connection, s3_client, s3_bucket))
        t.start()
        threads.append(t)

    # Wait for all tasks to be completed
    queue.join()

    # Optionally join threads if you want to wait for clean exit
    for t in threads:
        t.join()

    print("All files processed.")