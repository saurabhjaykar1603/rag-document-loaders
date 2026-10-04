from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

from langchain_community.document_loaders import TextLoader

loader = TextLoader(str(DATA_DIR / "rag_notes.txt"), encoding="utf-8")
docs = loader.load()

print("Documents:", len(docs))
print(docs[0].metadata)
print(docs[0].page_content)
