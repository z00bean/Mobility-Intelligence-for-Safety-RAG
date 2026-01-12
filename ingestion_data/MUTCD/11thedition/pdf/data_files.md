# Data Folder

This folder contains the **source data files** used by the knowledge base.

The data here is intended to be processed for tasks such as:
- Text extraction
- Chunking
- Embedding generation
- Indexing and retrieval

## What This Folder Contains

This folder may include multiple types of files, such as:

- **PDF documents**
- **Text files**
- **Images**
- Other supported raw content formats

Each data file can optionally have a corresponding metadata file (for example, a `metadata.json`) that provides additional context about the document.

## Chunking and Embedding

When used in a knowledge base or retrieval system:

- Documents may be **chunked** into smaller text segments to improve retrieval quality.
- These chunks can then be converted into **vector embeddings** for semantic search and similarity matching.
- Images may be processed separately or linked to extracted text, depending on the ingestion pipeline.

This folder stores only the **raw input files**, not the processed chunks or embeddings.

## Relationship to Metadata

If metadata is present, it typically:
- Lives alongside the data files (for example, in a `metadata/` directory)
- Describes attributes of the original document, not the generated embeddings
- Is used during ingestion to enrich or filter search results
