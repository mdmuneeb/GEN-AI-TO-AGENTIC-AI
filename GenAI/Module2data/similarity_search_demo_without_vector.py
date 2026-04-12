from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)

documents = [
    "Babar Azam is the captain of Pakistan cricket team and known for his elegant batting.",
    "Shaheen Afridi is a left-arm fast bowler famous for his pace and swing.",
    "Shahid Afridi, also known as Boom Boom, is remembered for his aggressive batting.",
    "Wasim Akram, the Sultan of Swing, is regarded as one of the greatest fast bowlers.",
    "Shoaib Malik has been a versatile all-rounder for Pakistan cricket over the years."
]

query = "tell me about shaheen afridi"

doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

scores = cosine_similarity([query_embedding], doc_embeddings)[0]
index, score = sorted(list(enumerate(scores)), key=lambda x: x[1])[-1]

print("Query:", query)
print("Most relevant document:", documents[index])
print("Similarity score:", score)