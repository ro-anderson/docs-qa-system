# Specialized AI Agents

The AI agents system consists of three specialized agents that work together to provide comprehensive assistance across different domains. Each agent is designed with specific expertise and uses RAG (Retrieval Augmented Generation) to provide accurate, contextual responses based on the processed document collections.

## Architecture

```
agents/
├── hr_policies_agent.py      # HR Policies specialist
├── labor_rules_agent.py      # Labor Rules specialist  
├── product_manual_agent.py   # Product Manual specialist
├── __init__.py              # Package initialization
└── README.md               # This documentation
```

## Agent Specialists

### HR Policies Agent (`hr_policies_agent.py`)

**Collection**: `hr_policies`  
**Expertise**: Company policies, employee procedures, benefits, HR guidelines

#### Capabilities
- Employee handbook questions
- Policy interpretation and clarification
- Benefits and compensation inquiries
- Procedure guidance (leave, performance reviews, etc.)
- Company culture and values information
- Onboarding and training procedures

#### Example Questions
```
✅ "What's our vacation policy?"
✅ "How do I request parental leave?"
✅ "What are the performance review procedures?"
✅ "What benefits are available to employees?"
✅ "How does the remote work policy work?"
```

#### Response Style
- Clear and helpful tone
- References specific policy sections
- Professional and supportive approach
- Asks for clarification when policies are ambiguous

---

### Labor Rules Agent (`labor_rules_agent.py`)

**Collection**: `labor_rules`  
**Expertise**: Employment law, worker rights, legal compliance, labor regulations

#### Capabilities
- Employment law interpretation
- Worker rights and employer obligations
- Workplace safety and health requirements
- Wage and hour law compliance
- Discrimination and harassment policies
- Union relations and collective bargaining
- Legal compliance requirements

#### Example Questions
```
✅ "What are the overtime regulations in Brazil?"
✅ "What are the legal requirements for termination?"
✅ "How do workplace safety regulations apply?"
✅ "What are the minimum wage requirements?"
✅ "What are the legal obligations for employee breaks?"
```

#### Response Style
- Accurate legal information
- References specific legal codes and statutes
- Distinguishes between federal, state, and local requirements
- Emphasizes compliance importance
- Recommends legal counsel for complex interpretations
- Includes educational disclaimers

---

### Product Manual Agent (`product_manual_agent.py`)

**Collection**: `product_manual`  
**Expertise**: Product documentation, technical support, installation guides, troubleshooting

#### Capabilities
- Product features and specifications
- Installation and setup instructions
- Troubleshooting and problem resolution
- Maintenance and care procedures
- Safety guidelines and warnings
- Technical specifications and compatibility
- Software configuration and settings

#### Example Questions
```
✅ "How do I install the new software?"
✅ "What are the system requirements?"
✅ "How do I troubleshoot connection issues?"
✅ "What's the maintenance schedule?"
✅ "How do I configure the settings?"
```

#### Response Style
- Clear step-by-step instructions
- References specific manual sections and page numbers
- Prioritizes safety information
- Uses technical language appropriately
- Organizes complex procedures into numbered steps
- Recommends professional service when appropriate

## Multi-Agent Coordination

### Team Structure
The agents work together through a coordinating team that:

1. **Analyzes Questions**: Determines which specialist(s) can best help
2. **Routes Intelligently**: Directs questions to appropriate agents
3. **Coordinates Responses**: Combines expertise when multiple domains overlap
4. **Handles Scope**: Politely declines out-of-scope questions
5. **Maintains Context**: Shares conversation history between agents

### Coordination Features
- **Agentic Context**: Shared understanding across all agents
- **Member Interactions**: Agents can reference each other's responses
- **History Management**: Remembers last 5 interactions for context
- **Datetime Awareness**: All agents have current time context
- **Streaming Responses**: Real-time answer generation

## Technical Implementation

### RAG Architecture
Each agent uses the same technical foundation:

```python
# Vector Database Connection
vector_db = PatchedQdrant(
    collection=collection_name,
    url=settings.QDRANT_URL,
    embedder=OpenAIEmbedder(),
)

# Knowledge Base
knowledge_base = AgentKnowledge(
    vector_db=vector_db, 
    num_documents=4
)

# Agent Creation
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge_base,
    add_references=True,
    markdown=True,
    instructions=specialized_instructions,
)
```

### Key Components

1. **OpenAI Embedder**: Uses text-embedding-ada-002 for query embeddings
2. **Qdrant Search**: Performs vector similarity search
3. **AgnoDoc Compatibility**: Custom document format for seamless integration
4. **Context Limiting**: Returns top 4 most relevant documents
5. **Reference Tracking**: Includes source attribution in responses

## Scope Management

### In-Scope Questions
Each agent handles questions within their domain:
- **HR Agent**: Company policies, procedures, benefits
- **Labor Agent**: Employment law, regulations, compliance
- **Product Agent**: Technical documentation, troubleshooting

### Out-of-Scope Handling
Questions outside all three domains are politely declined:
```
❌ "What's the weather today?"
❌ "Who won the football game?"
❌ "What's 2+2?"

Response: "I specialize in HR policies, labor laws, and product documentation. 
Could you rephrase your question to relate to one of these areas?"
```

## Performance Characteristics

### Response Quality
- **Accuracy**: High accuracy through specialized training
- **Relevance**: Vector search ensures contextual responses
- **Completeness**: Combines multiple document sources
- **Attribution**: Always includes source references

### Response Time
- **Query Processing**: ~1-2 seconds for vector search
- **Generation**: ~3-10 seconds for response generation
- **Streaming**: Real-time output as content is generated
- **Coordination**: Additional 1-2 seconds for multi-agent scenarios

### Resource Usage
- **Memory**: ~100MB per agent (models cached)
- **API Costs**: ~$0.01-0.05 per complex query
- **Vector Search**: ~10ms per collection search
- **Embeddings**: Real-time query embedding generation

## Configuration

### Environment Variables
```bash
# Model Configuration
CHAT_MODEL_ID=gpt-4o-mini          # OpenAI chat model
NUM_DOCUMENTS=4                    # Documents per search
NUM_HISTORY_RUNS=5                 # Conversation memory

# Display Configuration  
ENABLE_STREAMING=true              # Real-time responses
SHOW_MEMBERS_RESPONSES=true        # Show agent coordination
DEBUG_MODE=false                   # Debug logging
```

### Agent Customization
Each agent can be customized by modifying:
- **Instructions**: Update the system prompt
- **Knowledge Base**: Change document limit or search parameters
- **Model**: Switch between OpenAI models
- **References**: Enable/disable source attribution

## Usage Examples

### Single Agent Query
```
User: "What's our vacation policy?"
→ HR Policies Agent responds with policy details and references
```

### Multi-Agent Coordination
```
User: "What are the legal requirements for our company vacation policy?"
→ Coordinator consults both HR Policies and Labor Rules agents
→ Combined response with policy details + legal requirements
```

### Context-Aware Follow-up
```
User: "What's our vacation policy?"
Agent: [Provides vacation policy details]

User: "What if I need more time off?"
Agent: [References previous conversation, suggests additional leave options]
```

## Troubleshooting

### Common Issues

1. **No Relevant Documents Found**
   ```
   Issue: Agent returns "No relevant information found"
   Solution: Check if documents exist in correct collections
   Debug: Verify embeddings were created successfully
   ```

2. **Poor Response Quality**
   ```
   Issue: Generic or inaccurate responses
   Solution: Improve document quality and chunking strategy
   Debug: Review document content and embedding quality
   ```

3. **Agent Routing Issues**
   ```
   Issue: Questions go to wrong agent
   Solution: Refine coordinator instructions
   Debug: Check question classification logic
   ```

### Debug Mode
```bash
# Access chat service for debugging
make run-chat-cli-debug

# Inside container
python -c "from agents.hr_policies_agent import create_hr_policies_agent; agent = create_hr_policies_agent()"
```

## Best Practices

### Document Preparation
- **Structure**: Use clear headings and sections
- **Content**: Include comprehensive information
- **Format**: Maintain consistent markdown formatting
- **Updates**: Keep documents current and accurate

### Agent Usage
- **Specific Questions**: Ask targeted, specific questions
- **Context**: Provide sufficient context for complex queries
- **Follow-up**: Use follow-up questions to drill down
- **Scope**: Keep questions within agent expertise areas

### System Optimization
- **Collection Size**: Maintain manageable collection sizes
- **Document Quality**: Ensure high-quality source documents
- **Regular Updates**: Refresh embeddings when documents change
- **Monitor Performance**: Track response quality and speed

## Related Documentation

- **Main System**: [`../../../README.md`](../../../README.md)
- **Embedding Service**: [`../../../batch_embedder/app/embeddings/README.md`](../../../batch_embedder/app/embeddings/README.md)
- **Chat CLI Service**: [`../../README.md`](../../README.md)
- **Agno Framework**: [Agno Documentation](https://github.com/phidatahq/agno)
- **OpenAI Models**: [OpenAI Documentation](https://platform.openai.com/docs/models) 