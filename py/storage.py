import numpy as np
import pandas as pd
import fitz  
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm.notebook import tqdm
import urllib3


class VectorStore():
    def __init__(self, host, port):

        self.db = Elasticsearch([f"{host}:{port}"])
        
        # Test the connection
        try:
            if self.db.ping():
                print("Elasticsearch cluster is up!")
            else:
                print("Elasticsearch cluster is down!")
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {e}")

    def initialize_index(self, index_name, embedding_type, embedding_dim):
        index_mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {"type": embedding_type, "dims": embedding_dim}
                }
            }
        }
        if not self.db.indices.exists(index=index_name):
            self.db.indices.create(index=index_name, body=index_mapping)
        else:
            print('Elastic search index already exists')

    def index_text_chunks(self, index_name, embeddings):
        
        actions = [
            {
                '_index': index_name,
                '_id': f"{embedding_dict['doc_id']}_{embedding_dict['chunk_index']}",
                '_source': {
                    'text': embedding_dict['text'],
                    'embedding': embedding_dict['embedding']
                }
            }
            for embedding_dict in embeddings
        ]
        bulk(self.db, actions)
    
    def retrieve_documents(self, index_name, query_body):
        res = self.db.search(index=index_name, body=query_body)
        return [hit["_source"]["text"] for hit in res["hits"]["hits"]]
    



            