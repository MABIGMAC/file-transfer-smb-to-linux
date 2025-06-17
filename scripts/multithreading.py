import threading
import time

# Sample list of file paths (just dummy names for this example)
file_paths = [f"file_{i}.txt" for i in range(20)]

# Lock for synchronizing access to the shared list
list_lock = threading.Lock()

def process_file(thread_id):
    while True:
        with list_lock:
            if not file_paths:
                break
            file = file_paths.pop(0)
        # Simulate processing
        print(f"Thread {thread_id} processing {file}")
        time.sleep(0.1)  # Simulate time-consuming work

# Create and start threads
threads = []
for i in range(10):
    t = threading.Thread(target=process_file, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All files processed.")
