import os
import subprocess
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import chromadb
from langchain_mistralai import ChatMistralAI

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        exit(1)
    except FileNotFoundError:
        print(f"{script_name} not found. Please ensure it's in the current directory.")
        exit(1)

# Check and run necessary scripts
if not os.path.exists('cdp_documentation'):
    print("cdp_documentation folder not found. Running download.py...")
    run_script('download.py')

if not os.path.exists('./chroma_db'):
    print("chroma_db folder not found. Running embeddings.py...")
    run_script('embeddings_db.py')

# Load environment variables
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')

# Initialize the Chat model
model = ChatMistralAI(model="open-mistral-nemo", MISTRAL_API_KEY=api_key)

# Initialize ChromaDB client
persist_directory = "./chroma_db"
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_collection("cdp_documentation")

def get_advice(query):
    if not query:
        print('Query is required')
        return

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    relevant_docs = results['documents'][0]
    truncated_docs = [doc[:1000] for doc in relevant_docs]

    combined_input = (
        f"Here are some documents that might help answer the question: {query}\n\n"
        f"Relevant Documents:\n{chr(10).join(truncated_docs)}\n\n"
        "Please provide an answer based only on the provided documents.\n\n"
        "Your response should not be rude. Don't let the user know which document you are referring to.\n\n"
        "If you don't know the answer then refrain from answering anything!"
    )


    messages = [
        SystemMessage(content="""You are a Support Agent for Customer Data Platforms (CDPs). 
                                You provide guidance on how to perform tasks or achieve specific outcomes within Segment, mParticle, Lytics, and Zeotap.
                                Your answers should be clear, concise, and based on the provided documentation.
                                Follow these steps when answering:
                                1) Provide step-by-step instructions to achieve the task.
                                2) Mention any prerequisites or requirements.
                                3) Highlight any platform-specific considerations.
                                4) If the task is complex, break it into smaller steps.
                                5) Avoid technical jargon unless necessary, and explain it if used.
                                Your response should be easy to understand and actionable."""), 
        HumanMessage(content=combined_input),
    ]

    result = StrOutputParser().invoke(model.invoke(messages))
    print(result)

def main():
    print("Welcome to the CDP Support Assistant. Type 'exit' to end the program.")
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            print("Thank you for using the CDP Support Assistant. Goodbye!")
            break
        get_advice(query)

if __name__ == '__main__':
    main()
