from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

# Directory Loader
loader = DirectoryLoader(".\docs", glob="*.pdf", loader_cls=PyPDFLoader)
data = loader.load()

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
documents = text_splitter.split_documents(data)

# Add Ids with Documents
uuids = [str(uuid4()) for _ in range(len(documents))]


# Create Embeddings
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create Vector Instance 
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings_model,
    persist_directory="./chroma_db",
)

vector_store.add_documents(documents=documents, ids=uuids)

