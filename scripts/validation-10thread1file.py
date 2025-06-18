import threading
import time
import os

output_file = "shared_output.txt"
file_lock = threading.Lock()  # Optional — test with and without

NUM_THREADS = 10
LINES_PER_THREAD = 100

def write_lines(thread_id):
    for i in range(LINES_PER_THREAD):
        line = f"[Thread-{thread_id}] Line {i}\n"
        # Optional lock — try commenting this block out to test behavior
        with file_lock:
            with open(output_file, "a") as f:
                f.write(line)
        # time.sleep(0.001)  # Optional: slow down to increase concurrency

# Clear the output file
open(output_file, "w").close()

# Start threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=write_lines, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads
for t in threads:
    t.join()

print("Write complete. Validating...")

# Validation phase
expected_lines = NUM_THREADS * LINES_PER_THREAD
line_counts = {}

with open(output_file, "r") as f:
    lines = f.readlines()

# Check for total count
if len(lines) != expected_lines:
    print(f"[FAIL] Expected {expected_lines} lines, got {len(lines)}")

# Check line integrity
corrupt_lines = [line for line in lines if not line.startswith("[Thread-")]
if corrupt_lines:
    print(f"[FAIL] Found {len(corrupt_lines)} corrupt lines:")
    for line in corrupt_lines[:10]:
        print("  " + repr(line))
else:
    print("[PASS] No corrupt lines found.")

# Optionally count per-thread
for line in lines:
    if line.startswith("[Thread-"):
        thread_id = int(line.split("]")[0].split("-")[1])
        line_counts[thread_id] = line_counts.get(thread_id, 0) + 1

for i in range(NUM_THREADS):
    count = line_counts.get(i, 0)
    if count != LINES_PER_THREAD:
        print(f"[WARN] Thread {i} has {count} lines (expected {LINES_PER_THREAD})")
    else:
        print(f"[OK] Thread {i} wrote all lines")

print("Validation complete.")
