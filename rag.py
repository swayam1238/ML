import streamlit as st
import cohere
import faiss
import numpy as np
import pdfplumber

# Initialize Cohere client
cohere_api_key = "w0MZoCA0uGdMpLYoE6URut4S8FJEgGB1wRWOTYXj"  # Replace with your actual Cohere API key
co = cohere.Client(cohere_api_key)

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    """Extract text from the uploaded PDF."""
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to build FAISS index
def build_faiss_index(documents, model):
    """Build FAISS index from given documents."""
    embeddings = model.embed(texts=documents).embeddings
    embeddings = np.array(embeddings)
    index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance for similarity
    index.add(embeddings)
    return index, documents

# Function to query FAISS index
def query_faiss_index(query, index, documents, model, top_k=3):
    """Retrieve top-k relevant documents."""
    query_embedding = np.array(model.embed(texts=[query]).embeddings[0]).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    return [documents[i] for i in indices[0]]

# Function to generate text using Cohere with a word count check
def generate_response(query, context, min_words=150):
    """Generate a response based on a query and context."""
    prompt = (
        f"Use the following context to answer the query:\n\n"
        f"Context: {context}\n\n"
        f"Question: {query}\n\n"
        f"Answer with a detailed and informative summary of at least {min_words} words."
    )
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=700,  # Increased to ensure longer summaries
        temperature=0.7,
    )
    summary = response.generations[0].text.strip()
    
    # Ensure the summary is at least the minimum word count
    if len(summary.split()) < min_words:
        prompt += f"\n\nYour previous response was too short. Expand the summary to include more details."
        response = co.generate(
            model="command-xlarge-nightly",
            prompt=prompt,
            max_tokens=700,
            temperature=0.7,
        )
        summary = response.generations[0].text.strip()
    
    return summary

# Streamlit UI
st.set_page_config(page_title="PDF Summarizer", layout="wide")
st.title("PDF-Based Summarizer with RAG")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Build index when a file is uploaded
if uploaded_file:
    with st.spinner("Extracting text and building FAISS index..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        pdf_documents = [line.strip() for line in pdf_text.split("\n") if line.strip()]  # Split into individual lines
        st.session_state["index"], st.session_state["docs"] = build_faiss_index(pdf_documents, co)
    st.success("PDF processed and FAISS index built!")

# Text input for user query
user_query = st.text_area("Enter your query", placeholder="Summarize the section about dragons...")

# Button to generate summary
if st.button("Generate Summary"):
    if uploaded_file and user_query:
        with st.spinner("Retrieving relevant context and generating the summary..."):
            # Retrieve relevant context
            context_docs = query_faiss_index(user_query, st.session_state["index"], st.session_state["docs"], co)
            context = " ".join(context_docs)
            
            # Generate summary
            summary = generate_response(user_query, context, min_words=150)
            
            st.subheader("Generated Summary")
            st.write(summary)
    else:
        st.warning("Please upload a PDF and enter a query to generate a summary.")