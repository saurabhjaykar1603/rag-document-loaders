from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(str(DATA_DIR / "products.csv"), encoding="utf-8")
docs = loader.load()

print("Rows:", len(docs))
for doc in docs:
    print("\nMetadata:", doc.metadata)
    print(doc.page_content)
