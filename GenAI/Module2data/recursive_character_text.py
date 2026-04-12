from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create a recursive text splitter
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,                 # Target chunk size in characters
    chunk_overlap=100,              # Overlap between chunks
    separators=[
        "\n\n",     # First, try to split on double newlines (paragraphs)
        "\n",       # Then single newlines
        ". ",       # Then sentences
        ", ",       # Then clauses
        " ",        # Then words
        ""          # Finally, characters (last resort)
    ]
)

# Sample structured document
structured_document = """
# Introduction to RAG Systems

Retrieval-Augmented Generation represents a paradigm shift in how we build
AI applications. By combining retrieval mechanisms with generative models,
we can create systems that are both knowledgeable and creative.

## Key Benefits

RAG systems offer several advantages over traditional approaches:

1. Reduced hallucination through grounding in real documents
2. Easy knowledge updates without model retraining
3. Better source attribution and explainability
4. Cost-effective scaling of knowledge bases

## Implementation Considerations

When building a RAG system, you must consider:

- Chunk size optimization for your use case
- Embedding model selection based on your domain
- Vector database choice for your scale requirements
- Retrieval strategy tuning for precision vs recall

## Conclusion

Effective document chunking is foundational to RAG success. The strategy
you choose should align with your document types and query patterns.
"""

# Split the document recursively
recursive_chunks = recursive_splitter.split_text(structured_document)

# Display the chunks with their characteristics
for i, chunk in enumerate(recursive_chunks):
    print(f"Chunk {i + 1} (length: {len(chunk)} chars):")
    print(chunk)
    print("-" * 60)