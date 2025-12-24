# You will need to install: pip install langchain-community langchain-core
from langchain_community.llms import Ollama

# Initialize the Local LLM (Look no API keys! It's free!)
llm = Ollama(model="llama3") 

# The "Psychology" Test
response = llm.invoke("I am a user who says 'I guess the app is okay, but it's kinda confusing.' Analyze this statement for underlying emotion.")

print(response)
