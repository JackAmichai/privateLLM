from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class InsightVault:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.llm = Ollama(model="llama3")
        
        # Load the existing DB
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})

        # Psych-focused RAG Prompt
        self.template = """
        You are an expert User Researcher and Psychologist. 
        Your goal is to answer questions based ONLY on the following context from user interviews.
        
        If the answer is not in the context, say "I don't have enough data to answer that based on the interviews."
        
        Context:
        {context}
        
        Question:
        {question}
        
        Psychological Analysis:
        """
        
        self.prompt = ChatPromptTemplate.from_template(self.template)
        
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, query):
        print(f"🤔 Analyzing: {query}...")
        return self.chain.invoke(query)

if __name__ == "__main__":
    # Test the RAG pipeline
    vault = InsightVault()
    
    q1 = "What are the main frustrations users are facing?"
    print(f"\nUser: {q1}")
    print(f"Vault: {vault.ask(q1)}")
    
    q2 = "How do users feel about the dashboard?"
    print(f"\nUser: {q2}")
    print(f"Vault: {vault.ask(q2)}")
