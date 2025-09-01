import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(model="gpt-4.1")
prompt = """You are a helpful general purpose banking assistant.
Your task is to help users retrieve tasks, messages/notifications, and preferences from the ABN AMRO APIs.
You will use the tools provided by the MCP client to interact with these tools.
"""

load_dotenv()

client = MultiServerMCPClient(
    {
        "mcd": {
            "url": "http://127.0.0.1:10002/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
        "tasks": {
            "url": "http://127.0.0.1:10005/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
        "preferences": {
            "url": "http://127.0.0.1:10004/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
        "messages": {
            "url": "http://127.0.0.1:10003/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        }
    }
)

async def graph():
    tools = await client.get_tools()
    return create_react_agent(
        name="OperationsAgent",
        model=llm,
        prompt=prompt,
        tools=tools
    )