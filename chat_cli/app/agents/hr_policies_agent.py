# hr_policies_agent.py
"""
HR Policies RAG Agent (Agno + Qdrant) – OpenAI Embeddings
=========================================================
HR-specialized agent using:
* OpenAI embeddings instead of SentenceTransformer
* hr_policies collection
* Custom search with AgnoDoc compatibility
"""

from agno.agent import Agent, AgentKnowledge
from agno.models.openai import OpenAIChat

from core.settings import get_settings
from core.logger import logger
from vectordb.qdrant_factory import create_vector_db

settings = get_settings()

def create_hr_policies_agent() -> Agent:
    """Create and return the HR Policies specialist agent."""
    
    # Create vector database using factory
    vector_db = create_vector_db("hr_policies")
    
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