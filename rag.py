from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class InsightVault:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.llm = ChatOllama(model="llama3")
        
        # Load the existing DB
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # --- PROMPTS ---
        
        # 1. General Analysis
        self.template_general = """
        You are an expert User Researcher.
        Answer the question based ONLY on the following context.
        If the answer is not in the context, say so.
        
        Context:
        {context}
        
        Question:
        {question}
        """

        # 2. Sentiment Detective (Psych Focus)
        self.template_sentiment = """
        You are a Psychologist specialized in Micro-Expression and Text Analysis.
        Analyze the underlying EMOTIONS in the User's words from the context.
        
        Look for:
        - Hesitation (words like "I guess", "maybe", "kinda")
        - Hidden Frustration (polite complaints)
        - Anxiety or delight.
        
        Context:
        {context}
        
        Question: {question}
        
        Psychological Report:
        """

        # 3. The 5 Whys (Root Cause Analysis)
        self.template_5whys = """
        You are a Root Cause Analysis Agent using the "5 Whys" framework.
        Based on the user's feedback in the context, dig deep into WHY they feel this way.
        
        Chain of thought:
        1. Identify the surface problem.
        2. Ask "Why?" recursively to find the root technical or design cause.
        
        Context:
        {context}
        
        Question: {question}
        
        5 Whys Analysis:
        """

        self.prompts = {
            "General Analysis": ChatPromptTemplate.from_template(self.template_general),
            "Sentiment Detective": ChatPromptTemplate.from_template(self.template_sentiment),
            "The 5 Whys": ChatPromptTemplate.from_template(self.template_5whys)
        }

    def ask(self, query, mode="General Analysis"):
        print(f"🤔 Analyzing ({mode}): {query}...")
        
        # Select prompt based on mode
        prompt = self.prompts.get(mode, self.prompts["General Analysis"])
        
        chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain.invoke(query)

if __name__ == "__main__":
    # Test the RAG pipeline
    vault = InsightVault()
    
    q = "Whatever I don't care about the red badge."
    
    print("--- General ---")
    print(vault.ask(q, "General Analysis"))
    
    print("\n--- Sentiment ---")
    print(vault.ask(q, "Sentiment Detective"))
