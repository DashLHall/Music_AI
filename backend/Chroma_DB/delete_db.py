#used to delete db

import chromadb

def delete_collection_if_exists(client, name):
    try:
        client.delete_collection(name=name)
        print(f"Collection {name} deleted.")
    except :
        print(f"Collection {name} does not exist.")

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Delete the existing collection if it exists
delete_collection_if_exists(chroma_client, "music_data")