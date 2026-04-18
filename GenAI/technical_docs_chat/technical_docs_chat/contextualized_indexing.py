from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

# Directory Loader
loader = DirectoryLoader(".\docs", glob="*.pdf", loader_cls=PyPDFLoader)
pages = loader.load()  

# Contextualized Chunking
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
<document>{page_content}</document>

Here is the chunk we want to situate within the above page:
<chunk>{chunk_content}</chunk>

Give a short succinct context to situate this chunk within the page
for improving search retrieval. Answer only with the context, nothing else.
""")

chain = prompt | llm

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

contextualized_documents = []

for page in pages:
    chunks = text_splitter.split_documents([page])  

    for chunk in chunks:
        context = chain.invoke({
            "page_content": page.page_content,       # full page as reference
            "chunk_content": chunk.page_content       # chunk to situate
        }).content

        contextualized_documents.append(Document(
            page_content=f"{context}\n\n{chunk.page_content}",
            metadata=chunk.metadata
        ))

    print("=============Original Chunk=================")
    # print(chunks.page_content)
    print(chunk.page_content)
    print(f"✅ Page {page.metadata.get('page', '?')} → {len(chunks)} chunks contextualized")
    print("=============Contextualized Chunk=================")
    # print(contextualized_documents.page_content)
    print(context)



# Create Embeddings
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    persist_directory="./chroma_db",
)

vector_store.add_documents(
    documents=contextualized_documents,
    ids=[str(uuid4()) for _ in contextualized_documents]
)

print(f"\n✅ Indexed {len(contextualized_documents)} chunks into ChromaDB.")