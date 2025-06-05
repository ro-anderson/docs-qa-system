# product_manual_agent.py
"""
Product Manual RAG Agent (Agno + Qdrant) – OpenAI Embeddings
============================================================
Product Manual specialized agent using:
* OpenAI embeddings instead of SentenceTransformer
* product_manual collection
* Custom search with AgnoDoc compatibility
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from qdrant_client.http.models import Filter
from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.vectordb.qdrant import Qdrant as AgnoQdrant
from agno.embedder.openai import OpenAIEmbedder

from core.settings import get_settings
from core.logger import logger

settings = get_settings()

# ───────────────────── Document compatível ─────────────────────
@dataclass
class AgnoDoc:
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
            name = payload.get("name") or (text[:40].strip() or "product_manual_snippet")
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

def create_product_manual_agent() -> Agent:
    """Create and return the Product Manual specialist agent."""
    
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("Please set OPENAI_API_KEY environment variable")

    # Use OpenAI embedder instead of SentenceTransformer
    embedder = OpenAIEmbedder()

    vector_db = PatchedQdrant(
        collection=settings.COLLECTIONS["product_manual"],
        url=settings.QDRANT_URL,
        embedder=embedder,
    )

    knowledge_base = AgentKnowledge(vector_db=vector_db, num_documents=settings.NUM_DOCUMENTS)

    # Product Manual specialized agent
    agent = Agent(
        model=OpenAIChat(id=settings.CHAT_MODEL_ID),
        knowledge=knowledge_base,
        add_references=True,
        markdown=True,
        instructions="""You are a Product Manual and Technical Documentation Assistant. You specialize in helping users understand product features, installation procedures, troubleshooting issues, and technical specifications.

        Your expertise includes:
        - Product features and specifications
        - Installation and setup instructions
        - User guides and how-to procedures
        - Troubleshooting and problem resolution
        - Maintenance and care instructions
        - Safety guidelines and warnings
        - Technical specifications and compatibility
        - Software configuration and settings
        - Hardware connections and assembly
        - Warranty and support information
        
        When answering questions:
        - Provide clear, step-by-step instructions when applicable
        - Reference specific manual sections, page numbers, or diagrams when available
        - Prioritize safety information and warnings
        - Use simple, non-technical language when possible, but include technical details when necessary
        - Organize complex procedures into numbered steps or bullet points
        - Suggest checking specific model numbers or versions for compatibility
        - Recommend contacting technical support for hardware issues beyond basic troubleshooting
        - Always emphasize following manufacturer guidelines and safety precautions
        - If asked about topics outside product documentation, politely redirect to product-related matters
        
        Format your responses with:
        - Clear headings for different sections
        - Numbered steps for procedures
        - **Bold text** for important warnings or key information
        - Bullet points for lists of features or requirements
        
        Remember: Always prioritize user safety and recommend professional service when dealing with complex repairs or installations.
        """,
    )
    
    logger.info("Product Manual agent created successfully")
    return agent 