import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configuration
DATA_PATH = "data/rag_sample_qas_from_kis.csv" 
CHROMA_PATH = "backend/db/chroma_db"
TOP_K = 5 # number of chunks to return
MIN_SCORE = 0.7 # similarity threshold 

# OpenAI client setup
openai_client = OpenAI()

# Chroma client setup
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="rag_demo")

# Retrieves the top K similar documents for a given query
def retrieve(query, top_k=TOP_K, min_score=MIN_SCORE):
    # Embed query
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # Get top K results
    results = collection.query(
        query_embeddings=[emb],
        n_results=top_k,
        include=["metadatas", "distances", "documents"]
    )
    
    # Collect results above min_score, sort by similarity
    hits = []
    if results["documents"] and len(results["documents"]) > 0:
        for i, (doc, distance) in enumerate(zip(results["documents"][0], results["distances"][0])):
            similarity = distance  # Chroma returns distance
            print(f"Doc {i}: Distance: {distance}, Similarity: {similarity}")
            # Filter by min_score
            if similarity > min_score:
                hits.append({
                    "id": str(i),
                    "text": doc,
                    "similarity": similarity
                })

    return hits
