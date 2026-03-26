import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(data_folder="scraped_data"):
    documents = []

    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as f:
                doc_data = json.load(f)

            text_parts = [f"# {doc_data['title']}\nURL: {doc_data['url']}\n\n"]
            for section in doc_data.get('sections', []):
                heading_level = '#' * section['level']
                text_parts.append(f"{heading_level} {section['heading']}\n")
                for item in section.get('content', []):
                    if item['type'] == 'code':
                        text_parts.append(f"```\n{item['text']}\n```\n")
                    else:
                        text_parts.append(f"{item['text']}\n")
            if doc_data.get('standalone_text'):
                text_parts.append("\n".join(doc_data['standalone_text']))

            doc_text = "\n".join(text_parts)
            documents.append({"text": doc_text, "metadata": {"source": doc_data['url']}})

    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n## ", "\n### ", "\n", " ", ""]
    )

    all_chunks = []
    for doc in documents:
        chunks = splitter.create_documents([doc["text"]], metadatas=[doc["metadata"]])
        all_chunks.extend(chunks)

    return all_chunks
