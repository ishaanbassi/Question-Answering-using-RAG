
from tqdm import tqdm

def chunk_text(text, chunk_size=300):
    """Splits text into smaller chunks for embedding."""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def embed_text(text, embedding_model, tokenizer):
    """Generate embeddings for a text chunk."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    embeddings = embedding_model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.detach().numpy().tolist()[0]

def generate_embeddings(documents, embedding_model, tokenizer):
    
    embedding_list = []
    for raw_doc in tqdm(documents):
        for page in raw_doc:
            doc_id = page[0]
            text = page[1]
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                embedding = embed_text(chunk, embedding_model, tokenizer)
                embedding_list.append({
                    'doc_id': doc_id,
                    'chunk_index': i,
                    'text': chunk,
                    'embedding': embedding
                })

    return embedding_list        


