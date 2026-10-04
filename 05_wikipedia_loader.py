from langchain_community.document_loaders import WikipediaLoader

loader = WikipediaLoader(
    query="Python (programming language)",
    load_max_docs=3,
    doc_content_chars_max=12000,
)
docs = loader.load()

print("Articles:", len(docs))
for doc in docs:
    print("\nMetadata:", doc.metadata)
    print(doc.page_content)
