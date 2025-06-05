# rh_team_specialist.py
"""
RH Team Specialist - Multi-Agent Coordinator
============================================
Coordinates between specialized agents:
* HR Policies Agent 
* Labor Rules Agent
* Product Manual Agent

Uses Agno Team coordinate mode for intelligent query routing.
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team

from agents.hr_policies_agent import create_hr_policies_agent
from agents.labor_rules_agent import create_labor_rules_agent
from agents.product_manual_agent import create_product_manual_agent
from core.settings import get_settings
from core.logger import logger

settings = get_settings()

def create_rh_team() -> Team:
    """Create and return the RH specialist team."""
    
    logger.info("Creating RH Team Specialist...")
    
    # Create the specialized agents
    hr_specialist = create_hr_policies_agent()
    hr_specialist.name = "HR Policies Specialist"
    hr_specialist.role = "Specialist in company HR policies, procedures, and employee guidelines. Handles questions about company policies, employee benefits, procedures, and HR-related matters."
    hr_specialist.add_datetime_to_instructions = True
    
    labor_specialist = create_labor_rules_agent()
    labor_specialist.name = "Labor Rules Specialist"
    labor_specialist.role = "Expert in labor laws, employment regulations, and workplace compliance requirements. Handles questions about worker rights, employer obligations, legal compliance, and employment law."
    labor_specialist.add_datetime_to_instructions = True
    
    product_specialist = create_product_manual_agent()
    product_specialist.name = "Product Manual Specialist"
    product_specialist.role = "Expert in product documentation, technical manuals, and user guides. Handles questions about product features, installation, troubleshooting, and technical specifications."
    product_specialist.add_datetime_to_instructions = True

    # Create the coordinating team with enhanced settings
    rh_team = Team(
        name="RH Specialist Team",
        mode="coordinate",
        model=OpenAIChat(settings.CHAT_MODEL_ID),
        members=[hr_specialist, labor_specialist, product_specialist],
        description="You are a senior coordinator for specialized company assistance, managing expert consultations across HR policies, labor law, and product documentation.",
        instructions=[
            "You coordinate between three specialized experts to provide comprehensive company assistance.",
            "",
            "**Your specialist team includes:**",
            "- HR Policies Specialist: Company policies, employee procedures, benefits, HR guidelines",
            "- Labor Rules Specialist: Employment law, worker rights, legal compliance, labor regulations", 
            "- Product Manual Specialist: Product documentation, technical support, installation guides, troubleshooting",
            "",
            "**Coordination Protocol:**",
            "1. Analyze the user's question to determine which specialist(s) can best provide assistance",
            "2. For relevant questions, consult the appropriate specialist(s) and provide their expert guidance",
            "3. If multiple specialists are relevant, coordinate their responses for a comprehensive answer",
            "4. For questions completely outside these three domains (weather, sports, general knowledge, etc.), politely decline and redirect",
            "5. Always maintain context between interactions to provide consistent, informed assistance",
            "",
            "**For out-of-scope questions:**",
            "Explain that your team specializes exclusively in:",
            "- HR policies and company procedures",
            "- Labor laws and employment regulations", 
            "- Product manuals and technical documentation",
            "",
            "Guide users to rephrase questions within these specialized areas.",
            "",
            "**Quality Standards:**",
            "- Provide accurate, well-sourced information",
            "- Reference specific documentation when available", 
            "- Maintain professional, helpful tone",
            "- Ensure responses are comprehensive yet clear",
        ],
        add_datetime_to_instructions=True,
        add_member_tools_to_system_message=False,  # Better tool call consistency
        enable_agentic_context=True,  # Maintain shared context between specialists
        share_member_interactions=True,  # Share responses between members for better coordination
        show_members_responses=settings.SHOW_MEMBERS_RESPONSES,
        add_history_to_messages=True,
        num_history_runs=settings.NUM_HISTORY_RUNS,  # Remember last interactions
        markdown=True,
    )
    
    logger.info("RH Team Specialist created successfully")
    return rh_team 