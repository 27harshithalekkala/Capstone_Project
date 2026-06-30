from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(documents):
    """
    Split multiple PDF documents into chunks while preserving
    filename and page number metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunked_documents = []

    for document in documents:

        chunks = text_splitter.split_text(document["text"])

        for chunk in chunks:

            chunked_documents.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "page": document["page"]
                }
            )

    return chunked_documents