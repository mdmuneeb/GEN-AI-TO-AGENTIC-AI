from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# LLM
# ---------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------------------
# Embeddings (must match indexing)
# ---------------------------
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------------------
# Load Persistent Vector DB
# ---------------------------
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings_model,
    persist_directory="./chroma_db",
)

# ---------------------------
# Retriever 
# ---------------------------
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "lambda_mult": 0.5}
)

# ---------------------------
# Prompt
# ---------------------------
prompt = ChatPromptTemplate.from_template(
"""You are a domain expert assistant.

Answer using ONLY the provided context.

User question: {user_question}

Context:
{retrieved_passages}
"""
)

# ---------------------------
# Helper: format docs
# ---------------------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# ---------------------------
# RAG Chain (LCEL)
# ---------------------------
rag_chain = (
    {
        "retrieved_passages": retriever | format_docs,
        "user_question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# ---------------------------
# CLI Loop
# ---------------------------
while True:
    query = input("Enter Query: ")
    response = rag_chain.invoke(query)
    print("AI:", response)