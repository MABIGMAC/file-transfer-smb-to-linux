pip install pysmb

https://chatgpt.com/s/t_685926c85cf88191afccc184019a698d

# Set-up

1. Go to scripts/lib/env_var.py and change variables to suit your needs
2. Go to smb to s3.ipynb and run it (Single Threaded)

# Core libraries

> ## ~/scripts/lib:

* `env_var.py`: Environment variables for both s3 and smb to utilize, **please change this env** var before continuing
* `s3_client.py`: Seperated methods related to S3
* `smb_client.py`: Seperated methods related to SMB
* `utils.py`: methods not directly related to S3 or SMB

# Benchmarking 

> ## ~/benchmark results

Results of Put Object and Upload file are logged and recorded

Multi Thread results are in `upload_benchmark.csv` and ` benchmark_results1.csv `

inside the scripts folder has the scripts used to perform benchmarking
