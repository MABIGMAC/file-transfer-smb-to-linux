FROM cgr.dev/chainguard/python:latest-dev AS builder

# Environment configuration
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"
ENV JUPYTER_RUNTIME_DIR=/tmp/jupyter-runtime
ENV JUPYTER_DATA_DIR=/tmp/jupyter-data
ENV JUPYTER_CONFIG_DIR=/tmp/jupyter-config
ENV HOME=/home/jovyan

# Switch to root temporarily to set up filesystem
USER root

# Install Samba and Kerberos clients
RUN apk add --no-cache \
    krb5 \
    krb5-conf \
    cifs-utils \
    samba-client \
    samba-common-tools \
    keyutils \
    curl \
    bash \
    gcc \
    krb5-dev \
    python3-dev \
    py3-pip \
    libffi-dev \
    openssl-dev

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Create virtual environment and install dependencies
RUN python -m venv /venv && \
    mkdir -p /tmp/jupyter-runtime /tmp/jupyter-data /tmp/jupyter-config /home/jovyan && \
    chmod -R 0777 /tmp /home/jovyan

COPY requirements.txt /tmp
RUN pip install --no-cache-dir jupyterlab && \
    pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /home/jovyan

# Expose Jupyter port
EXPOSE 8888

# Entrypoint
ENTRYPOINT ["/venv/bin/jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]