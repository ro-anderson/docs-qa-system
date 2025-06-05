#!/usr/bin/env python3
"""
Chat CLI Main Application
========================
Main entry point for the RH Team Specialist chat interface.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.prompt import Prompt

from teams.rh_team_specialist import create_rh_team
from core.settings import get_settings
from core.logger import logger

console = Console()
settings = get_settings()

def main() -> None:
    """Main chat interface for RH Team Specialist."""
    
    try:
        logger.info("Starting Chat CLI application")
        
        # Create the RH team
        rh_team = create_rh_team()
        
        # Display welcome message
        console.print("[bold green]🏢 RH Team Specialist - Multi-Agent Coordinator[/bold green]")
        console.print("\n[italic]Especialistas disponíveis:[/italic]")
        console.print("• [cyan]HR Policies[/cyan] - Políticas da empresa, procedimentos, benefícios")  
        console.print("• [yellow]Labor Rules[/yellow] - Leis trabalhistas, direitos, compliance")
        console.print("• [blue]Product Manual[/blue] - Manuais técnicos, instalação, troubleshooting")
        console.print("\n[dim]Digite 'sair' para encerrar.[/dim]\n")
        
        # Chat loop
        while True:
            try:
                question = Prompt.ask("[bold cyan]💬 Sua pergunta")
                
                if question.lower() in {"sair", "exit", "quit"}:
                    console.print("\n[dim]Até logo! 👋[/dim]")
                    logger.info("User requested exit")
                    break
                    
                console.print("\n[dim]🤔 Analisando e consultando especialistas...[/dim]\n")
                logger.info(f"Processing question: {question}")
                
                # Use print_response for better formatting and streaming
                rh_team.print_response(question, stream=settings.ENABLE_STREAMING)
                        
            except KeyboardInterrupt:
                console.print("\n\n[dim]Interrompido pelo usuário. Até logo! 👋[/dim]")
                logger.info("User interrupted with Ctrl+C")
                break
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}")
                console.print(f"\n[red]❌ Erro: {str(e)}[/red]")
                console.print("[yellow]⚠️  Tente reformular sua pergunta.[/yellow]")
                
            console.print("\n" + "─" * 80 + "\n")
            
    except Exception as e:
        logger.error(f"Critical error in main application: {str(e)}")
        console.print(f"[red]❌ Erro crítico: {str(e)}[/red]")
        console.print("Verifique as configurações e tente novamente.")

if __name__ == "__main__":
    main() 