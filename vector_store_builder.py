from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class KnowledgeBase:
    def __init__(self):
        self.docs_urls = [
    "https://docs.capillarytech.com/"
]

        self.vectorstore = self.load_docs()

    def load_docs(self):
        print("Scraping docs...")
        all_documents = []
        for url in self.docs_urls:
            print(f"🔍 Scraping {url}")
            loader = WebBaseLoader(url)
            try:
                documents = loader.load()
                print(f"✅ Scraped {url}")
                all_documents.extend(documents)
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")

        # Use HuggingFace embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(all_documents, embeddings)
        return db

    @property
    def retriever(self):
        return self.vectorstore.as_retriever()
