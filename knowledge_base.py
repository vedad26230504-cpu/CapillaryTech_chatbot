class KnowledgeBase:
    def __init__(self):
        self.docs_urls = [
    "https://docs.capillarytech.com/docs/loyalty-overview",
    "https://docs.capillarytech.com/docs/loyalty-sdk",
    "https://docs.capillarytech.com/docs/getting-started",
]
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

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = FAISS.from_documents(all_documents, embeddings)

    @property
    def retriever(self):
        return self.vectorstore.as_retriever()
