from core.logger import logger
from vectordb.vectordb import VectorDB

def main():
    """Main function to run the batch embedding process"""
    try:
        logger.info("Starting the batch embedder service")
        
        # Use VectorDB as a context manager for proper connection cleanup
        with VectorDB() as vectordb:
            # Process all documents and create embeddings
            vectordb.create_all_embeddings()
            
            # Verify collections were created successfully
            vectordb.verify_collections()
        
        logger.info("Batch embedding process completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred in batch embedder: {e}")
        raise e

if __name__ == "__main__":
    main()