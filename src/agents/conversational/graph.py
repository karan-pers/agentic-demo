import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph_supervisor import create_supervisor
from langgraph_supervisor.handoff import create_forward_message_tool
from src.agents.transactions.graph import graph as get_transactions_agent
from src.agents.payments.graph import graph as get_payments_agent
from src.agents.operations.graph import graph as get_operations_agent
from src.agents.knowledge.graph import graph as knowledge_agent

load_dotenv()

model = AzureChatOpenAI(model="gpt-4.1")

PROMPT = """
You are a helpful, general-purpose banking assistant and a team supervisor managing three specialized agents: TransactionsAgent, PaymentsAgent, and OperationsAgent.
Maintain a warm and friendly demeanor while assisting users. The user is seeking assistance with their banking needs, and using chat-based interactions, so make sure your responses are maximum 1-2 paragraphs.

Each agent has access to a set of powerful tools (APIs) for banking operations. Use the most relevant agent and tool to address user queries efficiently and accurately.

Agent & Tool Capabilities:

TransactionsAgent:
-Retrieve account balances and contract lists.
-List payment contracts.
-Fetch and filter transactions or spends (by type, date, amount, etc.).

PaymentsAgent:
-Execute payments.
-Access address book /account beneficiaries and payment models.
-Validate account holders and payment instructions.
-Get payment account number formats.

OperationsAgent:
-View/Edit customer data like name, email, phone numbers, address, date of birth.
-Handle customer representatives.
-List, delete, and manage customer tasks or approval requests.
-Retrieve, delete, and get details of customer messages.
-Get and update newsletter and user preferences.

KnowledgeAgent:
-Provide information and answer questions about banking products and services.
-Assist with FAQs and general inquiries.
-Guide users in using banking tools and resources, in a self-service manner.

Instructions:
1. Always select the most specific agent as per agent capabilities for the user's request.
2. If a query spans multiple domains, coordinate between agents as needed.
3. Respond with clear, concise, and actionable information, leveraging the full capabilities of your agent team.
"""

client = MultiServerMCPClient(
    {
        "time_server":{
            "command": "uvx",
            "transport": "stdio",
            "args": ["--native-tls","mcp-server-time","--local-timezone=Europe/Amsterdam"]
        },
        "mcd": {
            "url": "http://127.0.0.1:10002/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        }
    }
)


forwarding_tool = create_forward_message_tool("ConversationalAgent")

async def graph():
    """Create a supervisor agent that manages multiple agents. 
    This agent has capabilities of transaction insights and payments.
    """
    tools = await client.get_tools()
    all_tools = [forwarding_tool] + tools

    return create_supervisor(
        agents=[
            await get_transactions_agent(),
            await get_payments_agent(),
            await get_operations_agent(),
            knowledge_agent
        ],
        tools=all_tools,
        model=model,
        prompt=PROMPT,
        output_mode="full_history",
        supervisor_name="ConversationalAgent",
    ).compile(name="ConversationalAgent")