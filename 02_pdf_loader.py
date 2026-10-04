from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(str(DATA_DIR / "document_loading_guide.pdf"))
docs = loader.load()

print("Pages:", len(docs))
for doc in docs:
    print("\nMetadata:", doc.metadata)
    print(doc.page_content)
