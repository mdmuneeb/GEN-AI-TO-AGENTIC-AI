from uuid import uuid4
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    # Where to save data locally, remove if not necessary
    persist_directory="./chroma_langchain_db",
)

document_1 = Document(
    page_content=("I had chocolate chip pancakes and " 
    "scrambled eggs for breakfast this morning."),
    metadata={"source": "tweet"}
)
document_2 = Document(
    page_content=("The weather forecast for tomorrow "
    "is cloudy and overcast, with a high of 62 degrees."),
    metadata={"source": "news"}
)
documents = [
    document_1,
    document_2
]
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)