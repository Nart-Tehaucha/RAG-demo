import os
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()  

# Configuration
CSV_FILE_PATH = "backend/data/rag_sample_qas_from_kis.csv"  # Path to our Kaggle CSV
CHROMA_PATH = "backend/db/chroma_db"  # Path to our chromadb
CHUNK_SIZE = 200                   # characters per chunk
CHUNK_OVERLAP = 50                 # characters overlapping between chunks
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 


# Chroma client setup
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection_name = "rag_demo"
collection = chroma_client.get_or_create_collection(name=collection_name)

# OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

loader = CSVLoader(file_path=CSV_FILE_PATH)
documents = loader.load()


# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

chunks = text_splitter.split_documents(documents)  

# Create embeddings & store in Chroma
for i, chunk in enumerate(chunks):
    vector = openai_ef(chunk.page_content) # generates embedding
    collection.add(
        ids=[str(i)],
        metadatas=[{"source": CSV_FILE_PATH}],
        documents=[chunk.page_content],
        embeddings= vector
    )