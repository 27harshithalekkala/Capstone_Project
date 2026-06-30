import streamlit as st

from module.pdf_manager import save_uploaded_files
from module.pdf_reader import extract_text_from_pdfs
from module.text_chunker import chunk_text
from module.embeddings import generate_embeddings
from module.vector_store import create_vector_store
from module.vector_store import create_vector_store
from module.retriever import retrieve_chunks
from module.gemini_client import ask_gemini

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Enterprise Financial Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)


# -------------------------------
# Initialize Session State
# -------------------------------
if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None

    
# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.title("🏢 FinVista Capital")
    st.markdown("---")

    st.subheader("Navigation")
    st.write("🏠 Dashboard")
    st.write("📂 Upload Documents")
    st.write("💬 AI Assistant")
    st.write("📑 Source Citations")
    st.write("🕒 Chat History")

    st.markdown("---")
    st.info("Enterprise GenAI Capstone Project")

# -------------------------------
# Main Page
# -------------------------------

st.title("📊 Enterprise Financial Intelligence Assistant")
st.caption("Retrieval-Augmented Generation (RAG) based Financial Knowledge Assistant")

st.markdown("---")

left, right = st.columns([2, 1])

# =====================================
# LEFT PANEL
# =====================================

with left:

    st.subheader("📂 Upload Enterprise Documents")

    uploaded_files = st.file_uploader(
        "Upload Financial PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        # --------------------------------
        # Save Uploaded PDFs
        # --------------------------------
        saved_files = save_uploaded_files(uploaded_files)

        st.success("✅ Documents uploaded successfully!")

        st.subheader("📁 Uploaded Documents")

        for file in saved_files:
            st.write(f"📄 {file}")

        # --------------------------------
        # Extract Text
        # --------------------------------
        extracted_text = extract_text_from_pdfs(uploaded_files)

        st.markdown("---")
        st.subheader("📄 Extracted Text Preview")

        preview_text = ""

        for doc in extracted_text:
            preview_text += doc["text"] + "\n"

        st.text_area(
            "Preview",
            preview_text[:2000],
            height=250
        )
        # --------------------------------
        # Create Chunks
        # --------------------------------
        chunks = chunk_text(extracted_text)

        st.markdown("---")
        st.subheader("📚 Text Chunks")

        st.success(f"✅ Total Chunks Created: {len(chunks)}")

        if chunks:
            st.text_area(
                "First Chunk Preview",
                chunks[0]["text"],
                height=250
            )

        # --------------------------------
        # Generate Embeddings
        # --------------------------------
        embeddings = generate_embeddings(chunks)

        st.success("✅ Embeddings Generated Successfully!")

        # --------------------------------
        # Create FAISS Vector Store
        # --------------------------------
        index = create_vector_store(embeddings)
        st.session_state.index = index
        st.session_state.chunks = chunks
        st.success("✅ FAISS Vector Store Created Successfully!")

    st.markdown("---")

    st.subheader("💬 Ask Questions")

    question = st.text_input(
        "Ask anything about your uploaded documents"
    )

    if st.button("Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        elif st.session_state.index is None:
            st.warning("Please upload PDF documents first.")

        else:

            with st.spinner("🤖 Gemini is analyzing your documents..."):

                retrieved_chunks = retrieve_chunks(
                    question,
                    st.session_state.index,
                    st.session_state.chunks
                )

                context = "\n\n".join(
                chunk["text"] for chunk in retrieved_chunks
                                )

                answer = ask_gemini(
                    context=context,
                    question=question
                )

            st.markdown("---")

            st.subheader("🤖 AI Answer")

            st.success(answer)
            st.markdown("### 📄 Sources")

            shown = set()

            for chunk in retrieved_chunks:
                source = f"{chunk['source']} (Page {chunk['page']})"

                if source not in shown:
                    shown.add(source)
                    st.write(f"• {source}")

