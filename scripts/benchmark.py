import os
import time
import psutil
import csv
from boto3.s3.transfer import TransferConfig
from lib.env_var import *
from lib.s3_client import get_s3_resource, ensure_bucket_exists

# Setup
process = psutil.Process(os.getpid())
s3 = get_s3_resource()
bucket = ensure_bucket_exists(s3, BUCKET_NAME)

def get_resource_usage():
    mem_info = process.memory_info()
    cpu_percent = process.cpu_percent(interval=0.1)
    mem_rss_mb = mem_info.rss / (1024 * 1024)
    return cpu_percent, mem_rss_mb

def upload_file_with_threads(thread_count):
    print(f"\n🧵 Testing with {thread_count} threads...")

    config = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,
        max_concurrency=thread_count,
        multipart_chunksize=8 * 1024 * 1024,
        use_threads=True
    )

    # Measure CPU/Memory before
    cpu_before, mem_before = get_resource_usage()
    start = time.time()

    bucket.upload_file(LOCAL_FILE_PATH, S3_KEY, Config=config)

    end = time.time()
    duration = end - start

    # Measure CPU/Memory after
    cpu_after, mem_after = get_resource_usage()

    print(f"⏱️ Time taken: {duration:.2f} sec")
    print(f"📊 CPU: {cpu_after:.1f}% (was {cpu_before:.1f}%)")
    print(f"📊 Memory: {mem_after:.2f} MB (was {mem_before:.2f} MB)")

    return {
        "threads": thread_count,
        "duration_sec": round(duration, 2),
        "cpu_percent_before": round(cpu_before, 1),
        "cpu_percent_after": round(cpu_after, 1),
        "mem_mb_before": round(mem_before, 2),
        "mem_mb_after": round(mem_after, 2)
    }

def benchmark_and_save(thread_counts, output_csv="benchmark_results.csv"):
    results = []
    for t in thread_counts:
        result = upload_file_with_threads(t)
        results.append(result)

    # Optional: Save to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results saved to {output_csv}")

if __name__ == "__main__":
    benchmark_and_save(thread_counts=[1, 4, 8, 16])
