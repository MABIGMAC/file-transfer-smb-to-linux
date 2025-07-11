import threading
import time

# Shared lock for both printing and file writing
list_lock = threading.Lock()

# File to write thread completion
output_file = "completed.txt"

# Number of threads
NUM_THREADS = 5

# Reset the output file at the start
with open(output_file, "w") as f:
    f.write("")

def count_to_100(thread_id):
    for i in range(1, 101):
        with list_lock:
            print(f"Thread {thread_id}: {i}")
        time.sleep(0.01)  # simulate some delay

    # Once counting is done, write to the file (also protected by the lock)
    with list_lock:
        with open(output_file, "a") as f:
            f.write(f"Thread {thread_id} finished counting to 100.\n")
        print(f"Thread {thread_id} wrote completion to file.")

# Create and start threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=count_to_100, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("All threads finished.")
