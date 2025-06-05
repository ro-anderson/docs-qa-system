# Embedding Generation Service

The embedding generation service is responsible for processing documents, creating text chunks, and generating vector embeddings using OpenAI's text-embedding models. This service forms the foundation of the document Q&A system by converting textual content into searchable vector representations.

## Architecture

```
embeddings/
├── embedding_generator.py    # Main embedding generation logic
├── __init__.py              # Package initialization
└── README.md               # This documentation
```

## Processing Pipeline

### 1. Document Discovery
- Scans the `data/` directory for markdown (.md) files
- Organizes documents by folder structure:
  - `data/hr-policies/` → `hr_policies` collection
  - `data/labor-rules/` → `labor_rules` collection  
  - `data/product-manual/` → `product_manual` collection

### 2. Text Chunking
- **Strategy**: Recursive character text splitter
- **Chunk Size**: 300 characters (configurable via `CHUNK_SIZE`)
- **Overlap**: 20 characters (configurable via `CHUNK_OVERLAP`)
- **Purpose**: Ensures optimal embedding quality and retrieval precision

### 3. Embedding Generation
- **Model**: OpenAI `text-embedding-3-small` (configurable via `EMBEDDING_MODEL`)
- **Dimensions**: 1536 (fixed by OpenAI model)
- **Batch Processing**: Processes chunks in batches for efficiency
- **Rate Limiting**: Respects OpenAI API rate limits

### 4. Vector Storage
- **Database**: Qdrant vector database
- **Distance Metric**: Cosine similarity
- **Collections**: Automatically creates separate collections per document type
- **Metadata**: Stores document name, chunk index, and original text

## Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required | `sk-...` |
| `EMBEDDING_MODEL` | OpenAI embedding model | `text-embedding-3-small` | `text-embedding-3-large` |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` | `http://qdrant:6333` |
| `DATA_PATH` | Document directory path | `./data` | `/app/data` |
| `CHUNK_SIZE` | Text chunk size | `300` | `512` |
| `CHUNK_OVERLAP` | Chunk overlap size | `20` | `50` |

### Supported Models

| Model | Dimensions | Use Case |
|-------|------------|----------|
| `text-embedding-3-small` | 1536 | Balanced performance (recommended) |
| `text-embedding-3-large` | 3072 | Higher quality, slower processing |
| `text-embedding-ada-002` | 1536 | Legacy model (compatible) |

## Usage

### Direct Execution
```bash
# From the embeddings directory
cd batch_embedder/app
python -m embeddings.embedding_generator
```

### Docker Execution (Recommended)
```bash
# Process all documents
make run-embedder

# Debug mode
make run-embedder-debug
```

## Processing Details

### Document Processing Flow

1. **Health Check**: Verifies Qdrant connectivity
2. **Collection Setup**: Creates collections if they don't exist
3. **Document Reading**: Reads all .md files from data folders
4. **Text Chunking**: Splits documents into optimal-sized chunks
5. **Embedding Generation**: Creates vector embeddings via OpenAI API
6. **Vector Storage**: Stores embeddings with metadata in Qdrant
7. **Verification**: Confirms successful storage and collection statistics

### Chunk Metadata Structure

Each chunk is stored with the following metadata:
```json
{
    "text": "Original chunk text content",
    "document_name": "example-policy.md",
    "chunk_index": 0,
    "collection_type": "hr_policies",
    "processed_at": "2024-01-01T00:00:00Z"
}
```

### Performance Characteristics

- **Processing Speed**: ~10-50 docs/minute (depends on document size and API limits)
- **Memory Usage**: Minimal (streaming processing)
- **API Costs**: ~$0.0001 per 1K tokens (text-embedding-3-small)
- **Storage**: ~6KB per chunk in Qdrant

## Monitoring

### Logging
- **File**: `batch_embedder.log`
- **Level**: INFO (configurable)
- **Format**: Timestamp, service, level, message

### Key Metrics Logged
- Documents processed count
- Chunks created count  
- Embeddings generated count
- API request duration
- Storage success/failure rates
- Collection statistics

### Health Checks
```bash
# Check Qdrant connectivity
curl http://localhost:6333/health

# View collection status
curl http://localhost:6333/collections
```

## Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   ```
   Error: Invalid API key
   Solution: Check OPENAI_API_KEY in .env file
   ```

2. **Qdrant Connection Issues**
   ```
   Error: Connection refused to Qdrant
   Solution: Ensure Qdrant service is running
   ```

3. **No Documents Found**
   ```
   Error: No .md files found in data/
   Solution: Add markdown files to data/ subfolders
   ```

4. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   Solution: Wait and retry, or upgrade OpenAI plan
   ```

### Debug Mode

Access the container for debugging:
```bash
make run-embedder-debug

# Inside container
python embedding_generator.py --verbose
python -c "from embedding_generator import *; test_embedding()"
```

## Best Practices

### Document Preparation
- **Format**: Use markdown (.md) files
- **Structure**: Include clear headings and sections
- **Length**: Optimal document size: 1-10 pages
- **Content**: Ensure content is well-structured and coherent

### Chunking Strategy
- **Size**: 300 characters works well for Q&A
- **Overlap**: 20 characters maintains context
- **Boundaries**: Respect sentence/paragraph boundaries when possible

### Collection Organization
- **Naming**: Use descriptive collection names
- **Separation**: Keep different document types in separate collections
- **Consistency**: Maintain consistent naming conventions

## Maintenance

### Regular Tasks
- Monitor embedding costs and usage
- Update documents and re-process as needed
- Clean up old or outdated collections
- Monitor Qdrant storage usage

### Updating Documents
```bash
# Add new documents to data/ folders
# Re-run embedding pipeline
make run-embedder
```

### Performance Optimization
- Adjust chunk size based on document types
- Use batch processing for large document sets
- Consider text-embedding-3-large for higher quality
- Implement incremental processing for large datasets

## Related Documentation

- **Main System**: [`../../README.md`](../../README.md)
- **Chat Agents**: [`../../chat_cli/app/agents/README.md`](../../chat_cli/app/agents/README.md)
- **OpenAI Embeddings**: [OpenAI Documentation](https://platform.openai.com/docs/guides/embeddings)
- **Qdrant**: [Qdrant Documentation](https://qdrant.tech/documentation/) 