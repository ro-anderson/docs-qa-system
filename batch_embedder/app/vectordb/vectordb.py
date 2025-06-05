import os
import uuid
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from core.settings import get_settings
from core.logger import logger
from embeddings.embedding_generator import EmbeddingGenerator
from .chunkenizer import recursive_character_splitting
from .utils import get_current_timestamp, format_timestamp

class VectorDB:
    def __init__(self):
        self.settings = get_settings()
        self.embedding_generator = EmbeddingGenerator()
        self.client = None
        self.connect_to_qdrant()
        
    def connect_to_qdrant(self):
        """Connect to Qdrant vector database"""
        try:
            self.client = QdrantClient(url=self.settings.QDRANT_URL)
            logger.info(f"Connected to Qdrant at {self.settings.QDRANT_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            raise e
    
    def close(self):
        """Close the connection to Qdrant"""
        if self.client:
            try:
                self.client.close()
                logger.info("Closed Qdrant connection")
            except Exception as e:
                logger.warning(f"Error closing Qdrant connection: {str(e)}")
            finally:
                self.client = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure connection is closed"""
        self.close()
    
    def create_collection(self, collection_name: str):
        """Create a collection in Qdrant if it doesn't exist"""
        try:
            if self.client.collection_exists(collection_name):
                logger.info(f"Collection {collection_name} already exists")
                # Optionally delete and recreate for fresh start
                # self.client.delete_collection(collection_name)
                # logger.info(f"Deleted existing collection: {collection_name}")
            else:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # OpenAI text-embedding-3-small dimension
                )
                logger.info(f"Created new collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to create collection {collection_name}: {str(e)}")
            raise e
    
    def read_markdown_files(self, folder_path: str) -> list:
        """Read all markdown files from a folder"""
        documents = []
        folder = Path(folder_path)
        
        if not folder.exists():
            logger.error(f"Folder does not exist: {folder_path}")
            return documents
            
        for file_path in folder.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append({
                        'filename': file_path.name,
                        'filepath': str(file_path),
                        'content': content
                    })
                    logger.info(f"Read file: {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to read file {file_path}: {str(e)}")
                
        return documents
    
    def upsert_vector(self, collection_name: str, doc_id: str, chunk_text: str, 
                     embedding: list, filepath: str, chunk_index: int):
        """Insert or update a vector in the collection"""
        try:
            chunk_id = str(uuid.uuid4())
            timestamp = get_current_timestamp()
            
            payload = {
                "created_at": format_timestamp(timestamp),
                "updated_at": format_timestamp(timestamp),
                "filepath": filepath,
                "document_id": doc_id,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text,
                "filename": os.path.basename(filepath)
            }
            
            # Check if vector already exists
            search_result = self.client.search(
                collection_name=collection_name,
                query_vector=embedding,
                query_filter=Filter(
                    must=[
                        FieldCondition(key="document_id", match=MatchValue(value=doc_id)),
                        FieldCondition(key="chunk_index", match=MatchValue(value=chunk_index))
                    ]
                ),
                limit=1
            )
            
            if search_result:
                logger.info(f"Updating existing vector for doc_id: {doc_id}, chunk: {chunk_index}")
            else:
                logger.info(f"Inserting new vector for doc_id: {doc_id}, chunk: {chunk_index}")
            
            self.client.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(id=chunk_id, vector=embedding, payload=payload)
                ]
            )
            
        except Exception as e:
            logger.error(f"Failed to upsert vector: {str(e)}")
            raise e
    
    def process_documents_for_collection(self, folder_name: str, collection_name: str):
        """Process all documents in a folder and store in specified collection"""
        folder_path = os.path.join(self.settings.DATA_PATH, folder_name)
        logger.info(f"Processing documents from: {folder_path}")
        
        # Check if collection exists first
        if self.client.collection_exists(collection_name):
            logger.info(f"Collection {collection_name} already exists. Skipping processing.")
            return
        
        # Create collection
        self.create_collection(collection_name)
        
        # Read documents
        documents = self.read_markdown_files(folder_path)
        
        if not documents:
            logger.warning(f"No documents found in {folder_path}")
            return
        
        # Process each document
        for doc in documents:
            doc_id = f"{folder_name}_{doc['filename']}"
            logger.info(f"Processing document: {doc_id}")
            
            # Split into chunks
            chunks = recursive_character_splitting(doc['content'])
            
            # Generate embeddings and store
            for i, chunk in enumerate(chunks):
                try:
                    logger.info(f"Processing chunk {i+1}/{len(chunks)} for {doc_id}")
                    embedding = self.embedding_generator.generate_embedding(chunk)
                    self.upsert_vector(
                        collection_name=collection_name,
                        doc_id=doc_id,
                        chunk_text=chunk,
                        embedding=embedding,
                        filepath=doc['filepath'],
                        chunk_index=i
                    )
                except Exception as e:
                    logger.error(f"Failed to process chunk {i} for {doc_id}: {str(e)}")
        
        logger.info(f"Completed processing documents for collection: {collection_name}")
    
    def create_all_embeddings(self):
        """Process all document folders and create embeddings"""
        logger.info("Starting batch embedding process")
        
        for folder_name, collection_name in self.settings.COLLECTIONS.items():
            try:
                logger.info(f"Processing folder: {folder_name} -> collection: {collection_name}")
                self.process_documents_for_collection(folder_name, collection_name)
            except Exception as e:
                logger.error(f"Failed to process folder {folder_name}: {str(e)}")
        
        logger.info("Completed batch embedding process")
    
    def verify_collections(self):
        """Verify that collections were created and contain data"""
        logger.info("Verifying collections...")
        
        for folder_name, collection_name in self.settings.COLLECTIONS.items():
            try:
                if self.client.collection_exists(collection_name):
                    info = self.client.get_collection(collection_name)
                    logger.info(f"Collection {collection_name}: {info.points_count} points")
                else:
                    logger.warning(f"Collection {collection_name} does not exist")
            except Exception as e:
                logger.error(f"Failed to verify collection {collection_name}: {str(e)}")