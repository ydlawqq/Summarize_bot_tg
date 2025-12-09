import chromadb

client = chromadb.Client()

collection = client.create_collection("documents")


def addDocs(embeddings, chunks, metadata, ids):
    collection.add(embeddings=[embeddings], documents=[chunks], metadatas=[metadata], ids=[ids])
