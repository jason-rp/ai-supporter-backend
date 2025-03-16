from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

pc = Pinecone(api_key="xxx")

index_name = "support-knowledge"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # ada-002
        metric="cosine", 
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
print("Index created or already exists:", pc.list_indexes().names())

client = OpenAI(api_key="xxx")

index = pc.Index(index_name)

# faq = "What’s your refund policy?"
# faq_id = "faq1"

# embedding_response = client.embeddings.create(model="text-embedding-ada-002", input=faq)
# embedding = embedding_response.data[0].embedding

# index.upsert(vectors=[(faq_id, embedding, {"text": faq})])

query_embedding = client.embeddings.create(model="text-embedding-ada-002", input="Can I return this?").data[0].embedding
result = index.query(vector=query_embedding, top_k=1, include_metadata=True)
print("Query result:", result["matches"][0]["metadata"]["text"])