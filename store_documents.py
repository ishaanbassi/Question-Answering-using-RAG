import numpy as np
import pandas as pd
import fitz  
from transformers import AutoTokenizer, AutoModel, AutoModelForQuestionAnswering, pipeline
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import torch
import os
import json
from tqdm.notebook import tqdm
import urllib3
from py import embed, retrieval, storage
from py.utils import pdf_utils
import sys


def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

if __name__ == "__main__": 
    
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    config = json.load(open('config.json'))

    embedding_model = AutoModel.from_pretrained(config['EMBEDDING_MODEL']['embedder_model'])
    tokenizer = AutoTokenizer.from_pretrained(config['EMBEDDING_MODEL']['embedder_model'])


    elastic_config = config['ELASTIC']
    vector_store = storage.VectorStore(elastic_config['host'], 
                                       elastic_config['port'])
    
    vector_store.initialize_index(elastic_config['index_name'], 
                                  config['EMBEDDING_MODEL']['embedding_type'],
                                  config['EMBEDDING_MODEL']['embedding_dim']) 
    
    raw_data_path = config['PATHS']['data']
    document_path_list = absoluteFilePaths(raw_data_path)
    
    documents = []
    for pdf_path in document_path_list:
        doc = {
            'file_path': pdf_path,
        }
        text_data = pdf_utils.extract_text_from_pdf(pdf_path)
        documents.append(text_data)

    text_chunks = embed.generate_embeddings(documents, embedding_model, tokenizer)
    
    vector_store.index_text_chunks(elastic_config['index_name'], text_chunks)