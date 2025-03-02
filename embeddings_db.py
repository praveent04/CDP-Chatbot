import os
import chromadb
from sentence_transformers import SentenceTransformer

def load_and_vectorize_documents(directory, persist_directory):
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=persist_directory)
    
    # Create or get collection
    collection = client.get_or_create_collection("cdp_documentation")
    
    # Initialize SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    
                # Create embedding
                embedding = model.encode(content).tolist()
                
                # Add to ChromaDB
                collection.add(
                    ids=[filename],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[{"source": filename}]
                )
                print(f"Processed and added: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print(f"All documents processed and saved to {persist_directory}")

def main():
    input_dir = "cdp_documentation"
    persist_directory = "./chroma_db"
    
    load_and_vectorize_documents(input_dir, persist_directory)

if __name__ == '__main__':
    main()
