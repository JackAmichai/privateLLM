# PrivateLLM: InsightVault 

**Secure, Local, Privacy-First User Research Analysis**

InsightVault (PrivateLLM) is a Retrieval-Augmented Generation (RAG) application designed to analyze sensitive user data—such as interview transcripts and feedback—without ever sending data to the cloud. It runs entirely on your local machine using [Ollama](https://ollama.com) and Llama 3.

## 🚀 Key Features

*   **100% Local Execution**: Powered by Llama 3 running via Ollama. No API keys, no data leakage.
*   **Privacy-First RAG**: Your data stays in a local vector database (ChromaDB).
*   **Specialized Analysis Modes**:
    *   **General Analysis**: Standard Q&A about your data.
    *   **Sentiment Detective**: Psychological analysis focusing on micro-expressions and hidden emotions.
    *   **The 5 Whys**: Root cause analysis framework.
*   **Interactive UI**: Built with Streamlit for a clean, chat-based experience.

## 🛠️ Architecture

*   **LLM**: Llama 3 (via Ollama)
*   **Embeddings**: Nomic / Llama 3 (via Ollama)
*   **Vector DB**: ChromaDB (Persistent local storage)
*   **Frontend**: Streamlit
*   **Framework**: LangChain

## 📦 Installation

### Prerequisites

1.  **Ollama**: Download and install from [ollama.com](https://ollama.com).
2.  **Llama 3 Model**: Run the following in your terminal:
    ```bash
    ollama pull llama3
    ```
3.  **Python 3.9+**: Ensure Python is installed.

### Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/JackAmichai/privateLLM.git
    cd privateLLM
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

### 1. Ingest Data
Before asking questions, you need to "teach" the AI about your data.
```bash
python ingest.py
```
*This processes the documents and saves them to the local `chroma_db`.*

### 2. Run the App
Launch the secure web interface:
```bash
./run.sh
```
*Or manually: `streamlit run app.py`*

## 🔒 Security Note
This project is architected for **zero-trust** environments. Code execution, model inference, and data storage occur strictly on the metal of your device.

---

**Author**: Jack Amichai
