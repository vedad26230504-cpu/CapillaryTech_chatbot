# CapillaryTech_chatbot
CapillaryTech Documentation Chatbot
A smart, documentation-aware chatbot designed to assist developers and integrators with CapillaryTech's platform by answering queries based on scraped documentation.

Built using LangChain, HuggingFace Embeddings, and a hybrid hardcoded + retrieval-augmented generation setup. Runs on Google Colab.

Overview
This chatbot can answer questions related to CapillaryTech's developer documentation. It fetches answers either from:

Hardcoded polished responses for key demo questions (for speed and clarity)
Retrieval-based answers using embeddings and similarity search on scraped docs
Features
Hybrid response system (hardcoded + dynamic retrieval)
HuggingFace embeddings for local, cost-free vector search
Clean Google Colab setup (no external hosting required)
Optimized for efficient document handling and querying
Easy to modify or extend for any custom documentation
Setup (Google Colab)
open the Colab notebook directly.
Install dependencies:
pip install langchain sentence-transformers faiss-cpu
Add your scraped documentation.
Run the chatbot cells and start querying.

Demo Video Watch the quick walkthrough: (https://drive.google.com/file/d/1UZgELurgyIu4a8iPEZ1hFHv5RZXUTpTw/view?usp=sharing)

⭕️ Note on Documentation Size :

Due to the large size of CapillaryTech's documentation, loading the entire content into memory caused crashes and instability in Google Colab. To address this: Only the most relevant sections (e.g., API usage, integrations, SDKs) were selected and processed.

This ensured response accuracy while maintaining performance.

In production, the full documentation could be handled in batches or using a hosted vector store.

google collab link : https://colab.research.google.com/drive/1LTGfZZGEziNnRV0Mqnlx4V0X7Qyc-ykp?usp=sharing
