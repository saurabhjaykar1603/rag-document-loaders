"""Load text, PDF, CSV, web, or Wikipedia sources as LangChain documents."""

import argparse
import json
from pathlib import Path
import sys


def load_documents(kind, source, *, max_docs=1, encoding="utf-8", delimiter=","):
    """Return documents with page_content and source metadata."""
    from langchain_community.document_loaders import (
        CSVLoader, PyPDFLoader, TextLoader, WebBaseLoader, WikipediaLoader,
    )

    if kind in {"text", "pdf", "csv"}:
        path = Path(source).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        source = str(path)

    if kind == "text":
        loader = TextLoader(source, encoding=encoding)
    elif kind == "pdf":
        loader = PyPDFLoader(source)
    elif kind == "csv":
        loader = CSVLoader(source, encoding=encoding, csv_args={"delimiter": delimiter})
    elif kind == "web":
        if not source.startswith(("https://", "http://")):
            raise ValueError("Web sources must start with https:// or http://")
        loader = WebBaseLoader(source, requests_kwargs={"timeout": 30})
    elif kind == "wikipedia":
        if max_docs < 1:
            raise ValueError("max_docs must be at least 1")
        loader = WikipediaLoader(query=source, load_max_docs=max_docs)
    else:
        raise ValueError(f"Unknown source type: {kind}")
    return loader.load()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["text", "pdf", "csv", "web", "wikipedia"])
    parser.add_argument("source", help="File path, URL, or Wikipedia search query")
    parser.add_argument("--max-docs", type=int, default=1, help="Wikipedia result limit")
    parser.add_argument("--encoding", default="utf-8", help="Text and CSV file encoding")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter")
    parser.add_argument("--preview-chars", type=int, default=600)
    parser.add_argument("--output", type=Path, help="Save all content and metadata to JSON")
    args = parser.parse_args()
    if args.preview_chars < 0:
        parser.error("--preview-chars must be non-negative")
    if args.max_docs < 1:
        parser.error("--max-docs must be at least 1")
    if len(args.delimiter) != 1:
        parser.error("--delimiter must be a single character")

    try:
        docs = load_documents(
            args.kind, args.source, max_docs=args.max_docs,
            encoding=args.encoding, delimiter=args.delimiter,
        )
        print(f"Loaded {len(docs)} document(s).")
        for index, doc in enumerate(docs, start=1):
            print(f"\nDocument {index}")
            print(json.dumps(doc.metadata, ensure_ascii=False, default=str))
            print(doc.page_content[:args.preview_chars])
        if not docs:
            print("No documents returned. Try another source or search query.")
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps([
                    {"page_content": doc.page_content, "metadata": doc.metadata}
                    for doc in docs
                ], indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            print(f"\nSaved to {args.output}")
    except Exception as error:
        # Keep the CLI readable while leaving library calls free to raise errors.
        print(f"Could not load source ({type(error).__name__}): {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
