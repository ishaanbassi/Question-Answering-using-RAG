#!/bin/bash

/usr/local/elasticsearch/bin/elasticsearch &

echo "Waiting for Elasticsearch to start..."
until curl -s http://localhost:9200 > /dev/null; do
  echo "Elasticsearch is still initializing..."
  sleep 5
done

echo "Elasticsearch is up and running."

python store_documents.py 

python qa_api.py