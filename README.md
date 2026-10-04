# Document Loading with LangChain

These examples follow my document-loading notebook: import one loader, give it a source, call `.load()`, and inspect the text and metadata. Each source type has its own Python file, so I can run and change one example at a time.

## Setup

```bash
git clone https://github.com/saurabhjaykar1603/rag-document-loaders.git
cd rag-document-loaders
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The original environment used Python 3.14. On Windows, activate with `.venv\Scripts\activate`. No Groq or OpenAI API key is needed for these examples.

## 01. TextLoader

```bash
python 01_text_loader.py
```

Reads `data/rag_notes.txt`: eight sections covering source documents, PDF extraction, CSV rows, web pages, Wikipedia, chunking, and pipeline checks. It prints the document count, source metadata, and full text.

```python
loader = TextLoader(str(DATA_DIR / "rag_notes.txt"), encoding="utf-8")
docs = loader.load()
print(docs[0].page_content)
```

TextLoader normally returns one document for the whole file. Change the filename to try another UTF-8 text source.

## 02. PyPDFLoader

```bash
python 02_pdf_loader.py
```

Reads `data/document_loading_guide.pdf`, a four-page guide included for practice. The example prints the number of pages, metadata, and extracted content for every page.

```python
loader = PyPDFLoader(str(DATA_DIR / "document_loading_guide.pdf"))
docs = loader.load()
```

Each page becomes a separate document. Check the `page` field in metadata when tracing content back to a PDF. Scanned pages may need OCR, which this example does not include.

## 03. CSVLoader

```bash
python 03_csv_loader.py
```

Reads 40 fictional product records from `data/products.csv`. Columns include ID, product name, category, price, stock, and description. Every row becomes a document with column names and values; metadata records the source and row number.

```python
loader = CSVLoader(str(DATA_DIR / "products.csv"), encoding="utf-8")
docs = loader.load()
```

Try a different CSV by changing the path. For a different delimiter, pass `csv_args={"delimiter": ";"}` to the loader. Loading does not calculate totals or convert the rows into a typed database table.

## 04. WebBaseLoader

```bash
python 04_web_loader.py
```

Loads `https://www.example.com`, extracts HTML text, and prints metadata and content. Change `web_path` to load another publicly accessible page. The example identifies its requests with a User-Agent and uses a 30-second timeout.

This requires internet access. Pages requiring authentication or JavaScript may not return useful text. Navigation and footer text may appear in the extracted content.

## 05. WikipediaLoader

```bash
python 05_wikipedia_loader.py
```

Searches for `Python (programming language)` and loads up to three articles, with a maximum of 12,000 characters per article. It prints article metadata and content.

```python
loader = WikipediaLoader(
    query="Python (programming language)",
    load_max_docs=3,
    doc_content_chars_max=12000,
)
docs = loader.load()
```

Check each article title and source: a search can return related or unrelated pages. If Wikipedia returns a blocked or non-JSON response, the dependency may raise `JSONDecodeError`; this is a request failure, not proof that the article does not exist.

## Run as a notebook

Open `5_rag_load_document.ipynb` in VS Code or Jupyter. Select your virtual environment as the kernel and run the sections in order. Run the notebook from the repository root so its `data/` paths resolve correctly.

The notebook contains the same five examples, with generic sources and no saved execution outputs. The standalone scripts resolve local data relative to their own location, so they also work when invoked from another directory.

## What the loader returns

Every example produces LangChain `Document` objects:

- `page_content`: the extracted text.
- `metadata`: source information such as path, page, row, URL, or title.

In the notebook, `docs` is reused by each section. Inspect it immediately after running that section to see that loader's results.

## Using this later in a RAG project

Start with the loader matching your source. Check the text and metadata, then split documents into chunks. Preserve metadata so an answer can cite its source. Next, create embeddings, store chunks in a vector database, retrieve relevant chunks, and pass them to a model.

Only document loading is implemented here. Chunking, embeddings, retrieval, and model responses are future steps.

An optional reusable command-line version is in `tools/document_loaders.py`. For example, to export the full text and metadata:

```bash
python tools/document_loaders.py text data/rag_notes.txt --output output/notes.json
```

Exports overwrite an existing file at the specified path. The `output/` directory is ignored by Git.

## Files

```text
01_text_loader.py
02_pdf_loader.py
03_csv_loader.py
04_web_loader.py
05_wikipedia_loader.py
5_rag_load_document.ipynb
data/
    rag_notes.txt
    document_loading_guide.pdf
    products.csv
tools/
    document_loaders.py
requirements.txt
```

The local text, PDF, and CSV examples are checked with the installed environment. Network examples depend on external services; a fresh dependency installation has not been checked. LangChain Community may show a deprecation warning.

All included data is generic practice material. CVs, appointment letters, credentials, and personal notebook outputs are not included.
