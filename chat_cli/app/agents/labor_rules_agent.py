# labor_rules_agent.py
"""
Labor Rules RAG Agent (Agno + Qdrant) – OpenAI Embeddings
=========================================================
Labor Rules specialized agent using:
* OpenAI embeddings instead of SentenceTransformer
* labor_rules collection
* Custom search with AgnoDoc compatibility
"""

from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat

from core.settings import get_settings
from core.logger import logger
from vectordb.qdrant_factory import create_vector_db

settings = get_settings()

def create_labor_rules_agent() -> Agent:
    """Create and return the Labor Rules specialist agent."""
    
    # Create vector database using factory
    vector_db = create_vector_db("labor_rules")
    
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