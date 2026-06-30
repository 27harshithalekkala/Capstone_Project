import faiss
import numpy as np


def create_vector_store(embeddings):
    """
    Create a FAISS vector store from embeddings.
    """

    # Convert embeddings to NumPy float32 array
    embeddings = np.array(embeddings, dtype="float32")

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS Index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to index
    index.add(embeddings)

    return index