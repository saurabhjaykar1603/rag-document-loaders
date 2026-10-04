import os

os.environ.setdefault("USER_AGENT", "RAGLoaderExamples/1.0 (https://github.com/saurabhjaykar1603/rag-document-loaders)")

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_path="https://www.example.com",
    requests_kwargs={"timeout": 30},
)
docs = loader.load()

print("Documents:", len(docs))
for doc in docs:
    print(doc.metadata)
    print(doc.page_content)
