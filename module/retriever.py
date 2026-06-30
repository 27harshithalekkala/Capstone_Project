from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(question, index, chunked_documents, top_k=3):
    """
    Retrieve the most relevant chunks along with
    filename and page number.
    """

    # Convert question into embedding
    question_embedding = model.encode([question]).astype("float32")

    # Search FAISS
    distances, indices = index.search(question_embedding, top_k)

    retrieved_documents = []

    for idx in indices[0]:

        if 0 <= idx < len(chunked_documents):

            retrieved_documents.append(
                {
                    "text": chunked_documents[idx]["text"],
                    "source": chunked_documents[idx]["source"],
                    "page": chunked_documents[idx]["page"]
                }
            )

    return retrieved_documents