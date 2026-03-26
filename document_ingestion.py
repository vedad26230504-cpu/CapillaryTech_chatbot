from langchain_community.document_loaders import WebBaseLoader

def ingest_docs(docs_urls):
    print("Scraping docs...")
    all_documents = []
    for url in docs_urls:
        print(f"🔍 Scraping {url}")
        loader = WebBaseLoader(url)
        try:
            documents = loader.load()
            print(f"✅ Scraped {url}")
            all_documents.extend(documents)
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
    return all_documents
docs_urls = [
    "https://developer.capillarytech.com/docs/loyalty-sdk-integration",
    "https://developer.capillarytech.com/docs/authentication-flows"
]
documents = ingest_docs(docs_urls)
