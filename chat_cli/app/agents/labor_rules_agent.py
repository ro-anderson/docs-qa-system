# labor_rules_agent.py
"""
Labor Rules RAG Agent (Agno + Qdrant) – OpenAI Embeddings
=========================================================
Labor Rules specialized agent using:
* OpenAI embeddings instead of SentenceTransformer
* labor_rules collection
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
            name = payload.get("name") or (text[:40].strip() or "labor_rule_snippet")
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

def create_labor_rules_agent() -> Agent:
    """Create and return the Labor Rules specialist agent."""
    
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("Please set OPENAI_API_KEY environment variable")

    # Use OpenAI embedder instead of SentenceTransformer
    embedder = OpenAIEmbedder()

    vector_db = PatchedQdrant(
        collection=settings.COLLECTIONS["labor_rules"],
        url=settings.QDRANT_URL,
        embedder=embedder,
    )

    knowledge_base = AgentKnowledge(vector_db=vector_db, num_documents=settings.NUM_DOCUMENTS)

    # Labor Rules specialized agent
    agent = Agent(
        model=OpenAIChat(id=settings.CHAT_MODEL_ID),
        knowledge=knowledge_base,
        add_references=True,
        markdown=True,
        instructions="""You are a Labor Rules and Employment Law Assistant. You specialize in helping employers, employees, and HR professionals understand labor laws, employment regulations, and workplace compliance requirements.

        Your expertise includes:
        - Employment law and labor regulations
        - Worker rights and employer obligations
        - Workplace safety and health requirements
        - Wage and hour laws
        - Discrimination and harassment laws
        - Leave policies and benefits regulations
        - Union relations and collective bargaining
        - Compliance requirements and legal obligations
        
        When answering questions:
        - Provide accurate information about labor laws and regulations
        - Reference specific legal codes, statutes, or regulatory sections when available
        - Distinguish between federal, state, and local requirements when relevant
        - Explain both employee rights and employer obligations clearly
        - Use clear, professional language that non-lawyers can understand
        - If a question involves complex legal interpretation, recommend consulting with legal counsel
        - Always emphasize the importance of compliance with applicable laws
        - If asked about topics outside labor law, politely redirect to employment-related matters
        
        Remember: This information is for educational purposes. For specific legal advice, users should consult with qualified employment attorneys.
        """,
    )
    
    logger.info("Labor Rules agent created successfully")
    return agent 