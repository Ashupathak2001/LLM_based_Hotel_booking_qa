import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

#  File paths
FAISS_INDEX_FILE = "faiss_index.bin"
DOCUMENTS_FILE = "documents.pkl"

#  Load the Sentence Transformer model
print("🔹 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

#  Check if FAISS index and documents exist
if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(DOCUMENTS_FILE):
    print("❌ Error: FAISS index or documents not found! Run `faiss_index.py` first.")
    exit()

#  Load FAISS Index
print("🔹 Loading FAISS index...")
faiss_index = faiss.read_index(FAISS_INDEX_FILE)

#  Load Stored Documents
print("🔹 Loading documents...")
with open(DOCUMENTS_FILE, "rb") as f:
    documents = pickle.load(f)
print(f"✅ Loaded {len(documents)} documents.")

def query_rag(question):
    print(f"🔹 Processing question: {question}")

    try:
        #  Generate embedding for the query
        query_embedding = model.encode([question], convert_to_numpy=True).astype('float32')

        #  Ensure FAISS index is not empty
        if faiss_index.ntotal == 0:
            print("❌ Error: FAISS index is empty! No data available for retrieval.")
            return "No relevant results found. The FAISS index is empty."

        #  Retrieve top 5 most relevant results from FAISS
        _, indices = faiss_index.search(query_embedding, k=5)

        #  Fetch the matched documents
        retrieved_docs = [documents[i] for i in indices[0] if i < len(documents)]

        if not retrieved_docs:
            print("❌ No relevant results found.")
            return "No relevant results found."

        #  Format the response
        context = "\n".join(retrieved_docs)
        response = f"Based on retrieved data:\n{context}\n\nAnswer: Further processing required."
        print("✅ Query processed successfully.")
        return response

    except Exception as e:
        print(f"❌ Error in query_rag(): {e}")
        return f"Error processing request: {e}"
