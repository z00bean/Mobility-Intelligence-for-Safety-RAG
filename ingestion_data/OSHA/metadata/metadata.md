# Metadata Folder

This folder contains **metadata files** associated with data files used in the knowledge base.

Metadata provides structured information *about* a document, rather than the document’s content itself.

## What Is Metadata in This Context?

In this repository, metadata is used to describe properties of a data file, such as:

- Document title or name
- Source or origin
- Document type
- Creation or update timestamps
- Tags or categories
- Any custom attributes required by the ingestion process

Metadata is commonly stored in a `metadata.json` file that corresponds to a specific document.

## Purpose of Metadata

Metadata can be used to:

- Enrich search and retrieval results
- Filter or scope queries
- Provide context to downstream systems
- Maintain traceability between raw files and their sources

## Relationship to Embeddings

- Metadata is **not embedded** as vector content by default.
- Instead, it is typically stored alongside embeddings and used for:
  - Filtering results
  - Displaying document information
  - Applying access or grouping logic

## Important Notes

- Metadata describes the **original data file**, not the chunked or embedded output.
- The exact metadata schema depends on the ingestion pipeline or knowledge base configuration.
- This folder does not contain embeddings or processed chunks.
