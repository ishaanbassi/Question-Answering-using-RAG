import openai

def retrieve_relevant_chunks(question_embedding, vector_store, index_name, top_k=3):
    """Retrieve top K most relevant chunks based on the question."""
    
    query_body = {
        "size": top_k,
        "_source": ["text"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": question_embedding}
                }
            }
        }
    }

    return vector_store.retrieve_documents(index_name, query_body)

def generate_answer(question, context, generation_config):
    
    prompt = f"Answer the following question in detail based on the context provided:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    response = openai.ChatCompletion.create(
        model=generation_config['generation_model'],  
        messages = [{'role': 'user', 'content': prompt}],
        max_tokens=generation_config['generation_max_token'],            
        temperature=generation_config['generation_temperature']             
    )
    return response.choices[0].message['content'].strip()



