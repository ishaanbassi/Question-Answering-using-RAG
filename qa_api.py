from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel, AutoModelForQuestionAnswering, pipeline
from elasticsearch import Elasticsearch
from py import embed, retrieval, storage
import torch
import urllib3
import openai
import json
import sys

app = Flask(__name__)


def initialize_app(app, vector_store_pass, api_key):
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    app.api_config = json.load(open('config.json'))

    app.embedding_model = AutoModel.from_pretrained(app.api_config['EMBEDDING_MODEL']['embedder_model'])
    app.tokenizer = AutoTokenizer.from_pretrained(app.api_config['EMBEDDING_MODEL']['embedder_model'])

    elastic_config = app.api_config['ELASTIC']
    app.vector_store = storage.VectorStore(elastic_config['host'], 
                                       elastic_config['port'])
    
    openai.api_key = api_key


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Define the API route for RAG-based question answering
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "Question is required"}), 400

    generation_config = app.api_config['GENERATION_MODEL']
    question_embedding = embed.embed_text(question, app.embedding_model, app.tokenizer)
    context_passages = retrieval.retrieve_relevant_chunks(question_embedding, app.vector_store, app.api_config['ELASTIC']['index_name'], generation_config['max_context'])

    # Generate answer
    answer = retrieval.generate_answer(question, context_passages, generation_config)
    
    # Respond with answer and top context passages
    response = {
        "question": question,
        "answer": answer,
        "contexts": context_passages
    }
    
    return jsonify(response)

if __name__ == "__main__":

    openai_key = input('Enter OpenAI API key : ')
    initialize_app(app, None, openai_key)        
    
    app.run(host="0.0.0.0", port=9202, debug=False)
