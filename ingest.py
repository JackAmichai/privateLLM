from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# Initialize Embeddings
# We use llama3 for embeddings. Ensure 'ollama pull llama3' has been run.
embeddings = OllamaEmbeddings(model="llama3")

# Mock User Interview Data
# In a real app, this would come from recorded transcripts.
documents = [
    Document(
        page_content="I really find the new feature confusing. I tried to click the 'save' button but it didn't give me any feedback, so I clicked it three times.",
        metadata={"source": "interview_sub_001", "topic": "usability_issue"}
    ),
    Document(
        page_content="The dashboard is great, but I feel anxious when I see the red notification badge. It feels like I'm in trouble.",
        metadata={"source": "interview_sub_002", "topic": "emotional_response"}
    ),
    Document(
        page_content="I use this tool every day for work. It saves me about 2 hours a week, but I wish it had a dark mode because my eyes hurt at night.",
        metadata={"source": "interview_sub_003", "topic": "feature_request"}
    ),
    Document(
        page_content="Honestly, I don't trust the auto-save. I always manually export my data just in case.",
        metadata={"source": "interview_sub_001", "topic": "trust_issue"}
    ),
]

def ingest_data():
    print("🚀 Starting Ingestion...")
    
    # Create/Persist ChromaDB
    # This will create a folder 'chroma_db' in the current directory
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    print(f"✅ Ingested {len(documents)} documents into ChromaDB.")

if __name__ == "__main__":
    ingest_data()
