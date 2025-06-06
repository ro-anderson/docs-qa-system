# Chat CLI Service - RH Team Specialist

A dockerized multi-agent chat interface that coordinates between specialized AI agents for company assistance.

## Architecture

```
chat_cli/
├── app/
│   ├── core/           # Core utilities
│   │   ├── logger.py   # Logging configuration  
│   │   └── settings.py # Environment settings
│   ├── agents/         # Specialized AI agents
│   │   ├── hr_policies_agent.py
│   │   ├── labor_rules_agent.py
│   │   └── product_manual_agent.py
│   ├── teams/          # Multi-agent coordinators
│   │   └── rh_team_specialist.py
│   └── main.py         # Application entry point
```

## Specialized Agents

### HR Policies Agent
- **Collection**: `hr_policies`
- **Expertise**: Company policies, employee procedures, benefits, HR guidelines
- **Use cases**: Policy questions, benefit inquiries, procedure clarification

### Labor Rules Agent  
- **Collection**: `labor_rules`
- **Expertise**: Employment law, worker rights, legal compliance, labor regulations
- **Use cases**: Legal compliance, employment law questions, worker rights

### Product Manual Agent
- **Collection**: `product_manual` 
- **Expertise**: Product documentation, technical support, installation guides
- **Use cases**: Product troubleshooting, installation help, technical specifications

## Usage

### Docker Compose (Recommended)

Start the chat interface:
```bash
docker compose up chat_cli
```

For debugging:
```bash
docker compose up chat_cli-bash
```

### Environment Configuration

Required environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333  # or http://qdrant:6333 in Docker
```

Optional configuration:
```bash
CHAT_MODEL_ID=gpt-4o-mini          # OpenAI model
NUM_DOCUMENTS=4                    # Documents per search
NUM_HISTORY_RUNS=5                 # Conversation memory
ENABLE_STREAMING=true              # Real-time responses
DEBUG_MODE=false                   # Debug logging
SHOW_MEMBERS_RESPONSES=true        # Show agent coordination
```

## Chat Interface

The interface provides:
- **Multi-agent coordination**: Automatically routes questions to appropriate specialists
- **Context awareness**: Maintains conversation history
- **Streaming responses**: Real-time answer generation  
- **Rich formatting**: Beautiful console output with emojis and colors
- **Error handling**: Graceful error recovery and user guidance

### Example Interactions

**HR Policy Question:**
```
💬  Your question: What's our vacation policy?
→ Routes to HR Policies Agent
```

**Labor Law Question:**
```  
💬 Your question: What are overtime regulations in Brazil?
→ Routes to Labor Rules Agent
```

**Product Question:**
```
💬 Your question: How do I install the new software?
→ Routes to Product Manual Agent
```

**Out-of-scope Question:**
```
💬 Your question: What's the weather today?
→ Politely declines and suggests relevant topics
```

## Technical Features

- **Agno Team Coordination**: Uses coordinate mode for intelligent routing
- **OpenAI Embeddings**: High-quality semantic search with text-embedding-ada-002
- **Qdrant Vector Database**: Efficient vector similarity search
- **Context Sharing**: Agents can reference each other's responses
- **History Management**: Maintains conversation context across interactions
- **Logging**: Comprehensive logging to `chat_cli.log`

## Troubleshooting

**Connection Issues:**
- Ensure Qdrant is running: `docker compose up qdrant`
- Verify OPENAI_API_KEY is set correctly
- Check network connectivity: `docker compose logs chat_cli`

**Agent Errors:**
- Verify collections exist in Qdrant
- Check embedding model availability
- Review logs: `docker compose logs chat_cli`

## Development

To extend the system:

1. **Add new agents**: Create in `agents/` folder with factory function
2. **Add new teams**: Create coordinator in `teams/` folder  
3. **Modify settings**: Update `core/settings.py` for new configurations
4. **Update main**: Modify `main.py` for new team integration 