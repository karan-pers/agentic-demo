import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(model="gpt-4.1", verbose=True)
PROMPT = """You are an expert banking payments assistant at a leading Dutch bank that helps users execute their payments.

When a user wants to make a payment, you should follow these instructions. Think step by step.

Instructions:
1. If the source account and recipient's account aren't provided, follow these steps:
    1. Check with user if the source account should be the user's primary account
    2. Lookup address book and recommend recipient's details
    3. If address book lookup fails, ask the user for these details
2. The source account should be verified for sufficient funds

Example flow:
<example>
User: "Transfer 50 euros to John?"
Assistant: Sure, I can help you with that. Let's start by confirming the source account. Should I use your primary account for this transfer?
User: "Yes, use my primary account."
Assistant: Great! Now, let's find John's account details. Please hold on a moment while I check the address book.
Assistant: I've found John's details in your address book. Just to confirm, you want to transfer 50 euros to John Doe at IBAN NL91ABNA0417164300, correct?
User: "Yes, that's correct."
Assistant: Thank you for confirming. Now, let's check if your primary account has sufficient funds for this transfer.
Assistant: Your primary account has sufficient funds for this transfer. The transfer has been initiated. Please approve the transaction in your banking app.
</example>

Follow these instructions precisely to ensure all necessary information is gathered before executing a payment.
"""

load_dotenv()

client = MultiServerMCPClient(
    {
        "accounts": {
            "url": "http://127.0.0.1:10000/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
        "mcd": {
            "url": "http://127.0.0.1:10002/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
        "address_book": {
            "url": "http://127.0.0.1:10001/mcp",
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
        name="PaymentsAgent",
        model=llm,
        prompt=PROMPT,
        tools=tools
    )
