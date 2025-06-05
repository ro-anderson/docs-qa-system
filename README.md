# Document Q&A System with Vector Database

A comprehensive Q&A chatbot system that processes documents and creates embeddings using OpenAI's embedding models, storing them in Qdrant vector database for efficient similarity search.

## Project Structure

```
.
├── batch_embedder/           # Batch embedding service
│   └── app/
│       ├── core/             # Core configuration and logging
│       │   ├── settings.py   # Environment configuration
│       │   └── logger.py     # Logging setup
│       ├── embeddings/       # Embedding generation
│       │   └── embedding_generator.py
│       ├── vectordb/         # Vector database operations
│       │   ├── vectordb.py   # Main VectorDB class
│       │   ├── chunkenizer.py # Text chunking utilities
│       │   └── utils.py      # Helper functions
│       └── main.py           # Entry point
├── data/                     # Document storage
│   ├── hr-policies/          # HR policy documents
│   ├── labor-rules/          # Labor rule documents
│   └── product-manual/       # Product manual documents
├── docker-compose.yml        # Docker services orchestration
├── Dockerfile               # Container definitions
├── pyproject.toml           # Python dependencies
└── .env.example             # Environment variables template
```

## Features

- **Multi-Collection Support**: Automatically creates separate Qdrant collections for different document types
- **OpenAI Integration**: Uses OpenAI's text-embedding-3-small model for high-quality embeddings
- **Document Chunking**: Intelligently splits documents using recursive character text splitter
- **Docker Support**: Fully containerized with Docker Compose orchestration
- **Health Checks**: Ensures Qdrant is ready before processing documents
- **Comprehensive Logging**: Detailed logging for monitoring and debugging

## Collections

The system automatically creates three collections in Qdrant:

1. **hr_policies** - For HR policy documents from `data/hr-policies/`
2. **labor_rules** - For labor rule documents from `data/labor-rules/`
3. **product_manual** - For product manual documents from `data/product-manual/`

## Setup

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd docs-qa-system
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

## Usage

### Start Qdrant Vector Database

```bash
docker compose up qdrant
```

This will start Qdrant on `http://localhost:6333` with a web UI available at `http://localhost:6333/dashboard`.

### Run Batch Embedding Process

```bash
docker compose up batch_embedder
```

This will:
1. Wait for Qdrant to be healthy
2. Read all markdown files from the `data/` folder
3. Create three collections in Qdrant
4. Process documents by chunking them
5. Generate embeddings using OpenAI
6. Store vectors in appropriate collections
7. Verify the collections were created successfully

### Run Both Services Together

```bash
docker compose up
```

### Debug Mode

To access the batch_embedder container for debugging:

```bash
docker compose run batch_embedder-bash
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | Required |
| `EMBEDDING_MODEL` | OpenAI embedding model | `text-embedding-3-small` |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `DATA_PATH` | Path to document folder | `./data` |
| `CHUNK_SIZE` | Text chunk size for splitting | `300` |
| `CHUNK_OVERLAP` | Overlap between chunks | `20` |

### Document Processing

- **Supported Formats**: Markdown (.md) files
- **Chunking Strategy**: Recursive character splitting with configurable size and overlap
- **Embedding Dimension**: 1536 (OpenAI text-embedding-3-small)
- **Vector Distance**: Cosine similarity

## Monitoring

### Logs

- Application logs are written to `batch_embedder.log`
- Console output shows real-time processing status
- Each document and chunk processing is logged

### Qdrant Dashboard

Access the Qdrant web interface at `http://localhost:6333/dashboard` to:
- View collections and their statistics
- Browse stored vectors
- Monitor system performance

## Development

### Local Development

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run locally:
   ```bash
   cd batch_embedder/app
   python main.py
   ```

### Adding New Document Types

1. Create a new folder in `data/`
2. Add the folder mapping in `batch_embedder/app/core/settings.py`:
   ```python
   COLLECTIONS = {
       "hr-policies": "hr_policies",
       "labor-rules": "labor_rules", 
       "product-manual": "product_manual",
       "new-folder": "new_collection"  # Add this line
   }
   ```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure your API key is correctly set in `.env`
2. **Qdrant Connection Error**: Make sure Qdrant service is running and healthy
3. **No Documents Found**: Check that markdown files exist in the data folders
4. **Permission Errors**: Ensure Docker has access to the project directory

### Logs Location

- Container logs: `docker compose logs batch_embedder`
- Application logs: `batch_embedder.log` file
- Qdrant logs: `docker compose logs qdrant`

## Next Steps

This batch embedder service provides the foundation for a Q&A system. Next steps could include:

1. **Query Service**: Create an API service for similarity search
2. **Chat Interface**: Build a web or chat interface
3. **RAG Pipeline**: Implement retrieval-augmented generation
4. **Authentication**: Add user authentication and authorization
5. **Monitoring**: Add metrics and monitoring dashboards