# hr_policies_agent.py
"""
HR Policies RAG Agent (Agno + Qdrant) – OpenAI Embeddings
=========================================================
HR-specialized agent using:
* OpenAI embeddings instead of SentenceTransformer
* hr_policies collection
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
            name = payload.get("name") or (text[:40].strip() or "hr_policy_snippet")
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

def create_hr_policies_agent() -> Agent:
    """Create and return the HR Policies specialist agent."""
    
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("Please set OPENAI_API_KEY environment variable")

    # Use OpenAI embedder instead of SentenceTransformer
    embedder = OpenAIEmbedder()

    vector_db = PatchedQdrant(
        collection=settings.COLLECTIONS["hr_policies"],
        url=settings.QDRANT_URL,
        embedder=embedder,
    )

    knowledge_base = AgentKnowledge(vector_db=vector_db, num_documents=settings.NUM_DOCUMENTS)

    # HR-specialized agent
    agent = Agent(
        model=OpenAIChat(id=settings.CHAT_MODEL_ID),
        knowledge=knowledge_base,
        add_references=True,
        markdown=True,
        instructions="""You are an HR Policies Assistant. You help employees understand company policies, procedures, and guidelines. 
        
        When answering questions:
        - Be clear and helpful about HR policies
        - Reference specific policy sections when relevant
        - If a policy is unclear or if you need more context, ask for clarification
        - Always maintain a professional and supportive tone
        - If asked about something outside HR policies, politely redirect to HR-related topics
        """,
    )
    
    logger.info("HR Policies agent created successfully")
    return agent 