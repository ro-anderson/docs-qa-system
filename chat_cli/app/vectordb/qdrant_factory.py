# qdrant_factory.py
"""
Qdrant Factory for Multi-Agent System
=====================================
Shared implementation of PatchedQdrant and AgnoDoc to eliminate code duplication
across all agents. This factory provides a consistent interface for vector database
operations with OpenAI embeddings.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from qdrant_client.http.models import Filter
from agno.vectordb.qdrant import Qdrant as AgnoQdrant
from agno.embedder.openai import OpenAIEmbedder

from core.settings import get_settings

settings = get_settings()

# ───────────────────── Document compatível ─────────────────────
@dataclass
class AgnoDoc:
    """Document class compatible with Agno framework."""
    id: str
    text: str
    metadata: Dict[str, Any]
    score: float
    name: str

    # Agno espera este método
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# ────────────────── Patched Qdrant (custom search) ─────────────────
class PatchedQdrant(AgnoQdrant):
    """Override search to preencher `name` e devolver `AgnoDoc`s."""

    def __init__(self, collection: str, default_snippet_name: str = "document_snippet", **kwargs):
        """Initialize PatchedQdrant with collection-specific default snippet name.
        
        Args:
            collection: The Qdrant collection name
            default_snippet_name: Default name for snippets when no name is found in metadata
            **kwargs: Additional arguments passed to parent class
        """
        super().__init__(collection=collection, **kwargs)
        self.default_snippet_name = default_snippet_name

    def search(  # type: ignore[override]
        self,
        query: str,
        limit: int = 4,
        filters: Optional[Filter] = None,
        **kwargs,
    ) -> List[AgnoDoc]:
        query_vector = self.embedder.get_embedding(query)
        kwargs.pop("filters", None)
        kwargs.pop("filter", None)

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=filters,
            **kwargs,
        )

        docs: List[AgnoDoc] = []
        for r in results:
            payload: Dict[str, Any] = r.payload or {}
            text = payload.get("text", "")
            name = payload.get("name") or (text[:40].strip() or self.default_snippet_name)
            docs.append(
                AgnoDoc(
                    id=str(r.id),
                    text=text,
                    metadata=payload,
                    score=r.score or 0.0,
                    name=name,
                )
            )
        return docs


def create_vector_db(collection_key: str) -> PatchedQdrant:
    """Factory function to create a PatchedQdrant instance for a specific collection.
    
    Args:
        collection_key: Key from settings.COLLECTIONS (e.g., 'hr_policies', 'labor_rules', 'product_manual')
        
    Returns:
        PatchedQdrant: Configured vector database instance
        
    Raises:
        RuntimeError: If OpenAI API key is not set
        KeyError: If collection_key is not found in settings.COLLECTIONS
    """
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("Please set OPENAI_API_KEY environment variable")
    
    if collection_key not in settings.COLLECTIONS:
        raise KeyError(f"Collection key '{collection_key}' not found in settings.COLLECTIONS")
    
    # Collection-specific default snippet names
    snippet_names = {
        "hr_policies": "hr_policy_snippet",
        "labor_rules": "labor_rule_snippet", 
        "product_manual": "product_manual_snippet"
    }
    
    # Use OpenAI embedder
    embedder = OpenAIEmbedder()
    
    # Create PatchedQdrant instance
    vector_db = PatchedQdrant(
        collection=settings.COLLECTIONS[collection_key],
        url=settings.QDRANT_URL,
        embedder=embedder,
        default_snippet_name=snippet_names.get(collection_key, "document_snippet")
    )
    
    return vector_db