# Base image with Python 3.8
FROM python:3.8-slim

# Set up environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg && \
    echo "deb http://deb.debian.org/debian buster main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian buster-updates main" >> /etc/apt/sources.list && \
    apt-get update

# Install system dependencies
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y build-essential && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y nano && \
    apt-get install -y vim && \
    apt-get install -y telnet && \
    apt-get install -y netcat-openbsd && \
    apt-get install -y procps && \
    rm -rf /var/lib/apt/lists/*

# Install Elasticsearch
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.0-linux-x86_64.tar.gz && \
    tar -xzf elasticsearch-7.10.0-linux-x86_64.tar.gz && \
    rm elasticsearch-7.10.0-linux-x86_64.tar.gz && \
    mv elasticsearch-7.10.0 /usr/local/elasticsearch

# Set environment variables for Elasticsearch
ENV ES_HOME=/usr/local/elasticsearch
ENV PATH="${ES_HOME}/bin:${PATH}"

# ARG DEVELOPER_UID=1001  # Replace with your actual UID from WSL
# ARG DEVELOPER_GID=1002

# RUN groupadd -g ${DEVELOPER_GID} developer && useradd -m -u ${DEVELOPER_UID} -g developer developer && \
RUN groupadd developer && useradd -m -g developer developer && \
    chown -R developer:developer /usr/local/elasticsearch && \
    chmod -R 775 /usr/local/elasticsearch

# 1
COPY . /workspaces/qa
RUN chown -R developer:developer /workspaces/qa

USER developer
WORKDIR /workspaces/qa

RUN chmod +x /workspaces/qa/run.sh

# Install Python dependencies
# COPY requirements.txt .

COPY .devcontainer/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose ports for Elasticsearch (9200) and any other services if needed
EXPOSE 9200 9201 9202

# Set the default command to a bash shell
CMD ["bash"]