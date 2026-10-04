# RAG Document Loaders

A Python script for loading text files, PDFs, CSV files, web pages, and Wikipedia articles into LangChain documents. It started as separate cells in `5_rag_load_document.ipynb`; the script makes that loading step reusable in future projects.

This project handles ingestion. It does not generate embeddings, search a vector database, or call an LLM. No model API key is needed.

## Setup

The original notebook environment used Python 3.14. Dependencies are pinned to the versions installed there.

```bash
git clone https://github.com/saurabhjaykar1603/rag-document-loaders.git
cd rag-document-loaders
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Usage

Run commands from the repository directory. Paths can be relative or absolute; quote paths containing spaces.

```bash
python document_loaders.py text examples/notes.txt
python document_loaders.py pdf "/path/to/resume.pdf"
python document_loaders.py csv examples/tasks.csv
python document_loaders.py web "https://www.example.com"
python document_loaders.py wikipedia "Python (programming language)" --max-docs 1
```

Replace the PDF path with your own file. The script prints the number of documents, their metadata, and a 600-character preview. `--preview-chars 1200` increases the preview without changing the loaded text.

Export the complete loaded documents to JSON:

```bash
python document_loaders.py text examples/notes.txt --output output/notes.json
```

The output directory is created if needed. An existing file at that path is replaced. Each JSON object contains `page_content` and `metadata`. The `output/` folder is ignored by Git.

For another CSV delimiter or encoding:

```bash
python document_loaders.py csv /path/to/data.csv --delimiter ";" --encoding utf-8
```

Run `python document_loaders.py --help` for all options.

## Implementation

The notebook followed the same pattern for each source: create a loader, call `.load()`, then inspect `page_content` and `metadata`. `load_documents()` keeps that pattern and chooses the loader using the input type.

| Source | Loader | Typical result |
| --- | --- | --- |
| Text | `TextLoader` | One document for the file |
| PDF | `PyPDFLoader` | One document per page |
| CSV | `CSVLoader` | One document per row |
| Web | `WebBaseLoader` | Extracted HTML text |
| Wikipedia | `WikipediaLoader` | Articles matching a search query |

Local paths are expanded and checked before loading. Web requests use a 30-second timeout. The CLI shows errors with exit code 1; the importable function raises errors so another application can handle them itself.

## Reuse in another project

```python
from document_loaders import load_documents

docs = load_documents("pdf", "/path/to/report.pdf")
for doc in docs:
    print(doc.metadata)
    print(doc.page_content[:200])
```

Add another loader inside `load_documents()` and add its type to the command-line choices to support more formats. Keep returning LangChain documents so later pipeline steps can use the same interface.

## Future RAG pipeline

1. Load source documents.
2. Split their content into overlapping chunks.
3. Create embeddings and store the chunks in a vector database.
4. Retrieve relevant chunks for a question.
5. Pass the retrieved text and source information to an LLM.

Only step 1 is implemented here. Splitting, embeddings, storage, retrieval, and answer generation are future additions.

## Limitations and troubleshooting

- Scanned PDFs may need OCR; OCR is not included.
- Web pages requiring JavaScript or authentication may not produce useful text.
- Wikipedia search results can be unrelated. Check article titles and source metadata.
- Wikipedia can return a non-JSON response and trigger `JSONDecodeError`. The CLI reports the failure; try again later or check API/network access.
- Wikipedia content has the loader's own length limit. `--preview-chars` only affects terminal output.
- CSV files need the correct delimiter and encoding.
- Text and metadata are printed to the terminal, and exports contain the source content.
- Network sources need internet access. Dependencies may emit a LangChain Community deprecation warning or a User-Agent notice.

## Project files

```text
document_loaders.py   Loader function and CLI
requirements.txt      Dependency versions
examples/notes.txt    Generic text sample
examples/tasks.csv   Generic CSV sample
README.md            Setup, usage, and future work
```

Text loading, CSV loading, JSON export, and CLI help were checked using the existing local environment. PDF and network loaders have not been exercised through this script, and a fresh dependency installation has not been verified.

Personal PDFs, downloaded datasets, credentials, and notebook outputs are excluded from this repository.
