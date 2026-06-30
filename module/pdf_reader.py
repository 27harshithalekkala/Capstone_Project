from pypdf import PdfReader


def extract_text_from_pdfs(uploaded_files):
    """
    Extract text from multiple uploaded PDF files
    along with filename and page number.
    """

    documents = []

    for file in uploaded_files:

        reader = PdfReader(file)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:

                documents.append(
                    {
                        "text": text,
                        "source": file.name,
                        "page": page_number
                    }
                )

    return documents