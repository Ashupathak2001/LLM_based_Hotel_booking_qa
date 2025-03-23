import os
import faiss
import pandas as pd
import numpy as np
import pickle
import time
from sentence_transformers import SentenceTransformer

#  File paths
FAISS_INDEX_FILE = "faiss_index.bin"
DOCUMENTS_FILE = "documents.pkl"
DATASET_FILE = "cleaned_hotel_bookings.csv"

#  Check if FAISS index and documents already exist
if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(DOCUMENTS_FILE):
    print("✅ FAISS index and documents already exist. Skipping embedding process.")
else:
    print("🔹 FAISS index or documents not found. Creating embeddings...")

    #  Load dataset
    if not os.path.exists(DATASET_FILE):
        print(f"❌ Error: Dataset '{DATASET_FILE}' not found!")
        exit()

    df = pd.read_csv(DATASET_FILE)
    print(f"✅ Successfully loaded {len(df)} records from dataset.")

    #  Load embedding model
    print("🔹 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    #  Convert Booking Data to Text
    def format_booking(row, max_length=200):
        text = f"Hotel: {row['hotel']}, Country: {row['country']}, Lead Time: {row['lead_time']} days, ADR: ${row['adr']}, Canceled: {bool(row['is_canceled'])}"
        return text[:max_length]

    documents = df.apply(format_booking, axis=1).tolist()

    #  Initialize FAISS Index
    dimension = 384  # MiniLM model outputs 384-dimensional vectors
    faiss_index = faiss.IndexFlatL2(dimension)

    #  Embed Documents in Batches (to prevent crashes)
    batch_size = 500
    embeddings = []
    print("🔹 Generating embeddings and storing in FAISS...")

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        try:
            batch_embeddings = model.encode(batch, convert_to_numpy=True).astype('float32')
            faiss_index.add(batch_embeddings)
            embeddings.extend(batch_embeddings)
            print(f"✅ Processed batch {i}-{i+batch_size}")
            time.sleep(1)  # Small delay to prevent overloading
        except Exception as e:
            print(f"❌ Error processing batch {i}-{i+batch_size}: {e}")

    #  Save FAISS Index & Documents
    faiss.write_index(faiss_index, FAISS_INDEX_FILE)
    with open(DOCUMENTS_FILE, "wb") as f:
        pickle.dump(documents, f)

    print("🎉 FAISS Indexing Complete! Data stored successfully.")
