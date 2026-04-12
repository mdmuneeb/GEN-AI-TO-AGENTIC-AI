from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    # Where to save data locally, remove if not necessary
    persist_directory="./chroma_langchain_db",
)
results = vector_store.similarity_search(
    "tell me about weather",
    k=1,
    # filter={"source": "tweet"},
)

print(results)