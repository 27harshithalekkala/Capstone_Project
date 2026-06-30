from sentence_transformers import SentenceTransformer

# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunked_documents):
    """
    Generate embeddings for chunked documents while preserving metadata.
    """

    # Extract only the text from each chunk
    texts = [doc["text"] for doc in chunked_documents]

    # Generate embeddings
    embeddings = model.encode(texts)

    return embeddings