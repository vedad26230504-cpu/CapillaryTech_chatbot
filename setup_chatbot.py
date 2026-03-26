def setup_chatbot():
    base_url = "https://docs.capillarytech.com/"
    scraper = DocumentationScraper(base_url)

    if not os.path.exists("scraped_data") or len(os.listdir("scraped_data")) == 0:
        print("Scraping docs...")
        scraper.crawl(max_pages=50)
    else:
        print("Using existing scraped data.")

    print("Loading and chunking documents...")
    raw_docs = load_documents()
    chunks = split_documents(raw_docs)

    kb = KnowledgeBase()
    if not os.path.exists("chroma_db") or not os.listdir("chroma_db"):
        print("Creating knowledge base...")
        kb.create_from_documents(chunks)
    else:
        print("Using existing knowledge base.")

    bot = DocumentationChatbot(kb)
    print(f"\n✅ Chatbot is ready! Loaded {len(raw_docs)} documents into {len(chunks)} chunks.")
    return bot
