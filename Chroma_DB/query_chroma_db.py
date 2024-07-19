# query_chroma_db.py

from chromadb import ChromaDBClient
from sentence_transformers import SentenceTransformer

# Initialize Chroma DB client
chroma_client = ChromaDBClient()

# Access the collection
collection = chroma_client.get_collection("songs")

# Initialize a sentence transformer model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Artist's name to search
artist_name = "Raphael Saadiq"

# Generate embedding for the artist's name
artist_embedding = model.encode([artist_name])[0]

# Query Chroma DB for similar song titles
results = collection.query(artist_embedding, k=10)  # k is the number of similar items to retrieve

# Print the results
for result in results:
    print(f"Title: {result['metadata']['title']}")
    print(f"Artist: {result['metadata']['artist']}")
    print(f"Similarity Score: {result['score']}")

if not results:
    print(f"No songs found for the artist: {artist_name}")