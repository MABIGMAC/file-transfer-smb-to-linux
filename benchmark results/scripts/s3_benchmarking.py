import os
import time
import psutil
import csv
from boto3.s3.transfer import TransferConfig
from lib.env_var import *
from lib.s3_client import get_s3_resource, ensure_bucket_exists

process = psutil.Process(os.getpid())
s3 = get_s3_resource()
bucket = ensure_bucket_exists(s3, BUCKET_NAME)

def get_resource_usage():
    mem = process.memory_info().rss / (1024 * 1024)
    cpu = process.cpu_percent(interval=0.1)
    return round(cpu, 2), round(mem, 2)

def upload_file_with_config(bucket, local_path, s3_key, concurrency, chunk_size_mb):
    print(f"🧪 Uploading with {concurrency} threads | {chunk_size_mb}MB chunks")

    part_size = chunk_size_mb * 1024 * 1024
    config = TransferConfig(
        multipart_threshold=part_size,  # force multipart always
        multipart_chunksize=part_size,
        max_concurrency=concurrency,
        use_threads=True
    )

    cpu_before, mem_before = get_resource_usage()
    start = time.time()

    bucket.upload_file(local_path, s3_key, Config=config)

    duration = time.time() - start
    cpu_after, mem_after = get_resource_usage()

    return {
        "threads": concurrency,
        "chunk_mb": chunk_size_mb,
        "duration_sec": round(duration, 2),
        "cpu_before": cpu_before,
        "cpu_after": cpu_after,
        "mem_before_mb": mem_before,
        "mem_after_mb": mem_after
    }

def run_benchmark(thread_options, chunk_options, output_csv="upload_benchmark.csv"):
    results = []
    for threads in thread_options:
        for chunk in chunk_options:
            key = f"benchmark/{threads}t_{chunk}mb_{os.path.basename(LOCAL_FILE_PATH)}"
            result = upload_file_with_config(bucket, LOCAL_FILE_PATH, key, threads, chunk)
            results.append(result)

    # Write to CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Benchmark results saved to {output_csv}")

if __name__ == "__main__":
    thread_counts = [ 8, 16, 32, 64]
    chunk_sizes_mb = [8, 16, 32]
    run_benchmark(thread_counts, chunk_sizes_mb)
