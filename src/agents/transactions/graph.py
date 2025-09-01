import os
import datetime
import pytz
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(model="gpt-4.1", verbose=True)
PROMPT = """You are an expert transaction banking assistant at a leading Dutch bank that helps users with their financial transactions.

[Important]

For any questions related to date and time, always use the get_current_time tool to get the current day, month, year and time instead of relying on your internal clock.
Remember, current year is 2025 !
You have an MCP tool called get_transactions which retrieves transactions in a paginated way using a last_mutation_key. Your task is to fetch and aggregate transactions completely based on the user's date range query, handling pagination automatically.

Instructions:

1. Think step by step. Most people use 'Personal Account' for their main account.

2. [Critical] Parse the user's query for the account number and date range (<start_date> & <end_date>):
    1. You cannot lookup transactions for future dates.
    2. If date range isn't clear, clarify with the user.
    3. <end_date> is always exclusive, meaning transactions on that date are not included.
    4. <end_date> cannot be later than the current date.

3. Call the get_transactions tool with the account_number and include_actions set to "EXTENDED". For the initial call, do not pass last_mutation_key.

4. Collect transactions from the response and filter them by the parsed date range if the tool does not provide native filtering by date.

5. If the response includes a lastMutationKey indicating more pages of transactions exist, recursively call get_transactions again with the same parameters plus the returned last_mutation_key.

6. Repeat step 3 and 4 until the lastMutationKey is null, meaning all pages have been fetched.

7. After collecting all pages, aggregate the spending amount (sum of all transactions' relevant values) within the date range.

8. Respond to the user with the total spending amount and the covered date range.

Example flow:
<example>
User: "How much did I spend in <current_month>?"
Assistant:

Calculate the days elapsed in the month, with <startdate> as the first day of the month and <enddate> as the current date.

Convert these dates to 00:00:00 time timestamps (in ms).

Call get_transactions(account_number, include_actions="EXTENDED", transaction_type="DEBIT", book_date_from = <startdate_timestamp> , book_date_to= <enddate_timestamp>).

While last_mutation_key is present, recurse with that key.

Sum all filtered transactions.

Reply with total spending last month.
</example>

Follow these instructions precisely for any spending amount query to ensure all paginated data is fetched and aggregated before answering.
"""

load_dotenv()

@tool
def convert_europe_amsterdam_to_unix(datetime_str: str) -> int:
    """
    Converts a datetime string in Europe/Amsterdam timezone (e.g. '2025-07-01 00:00:00') to UNIX timestamp in milliseconds.
    Accepts formats like 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'.
    """
    tz = pytz.timezone('Europe/Amsterdam')
    try:
        dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d")
    dt = tz.localize(dt)
    return int(dt.timestamp() * 1000)

client = MultiServerMCPClient(
    {
        "accounts": {
            "url": "http://127.0.0.1:10000/mcp",
            "transport": "streamable_http",
            "headers": {
                "cookie": os.getenv("cookie", "")
            }
        },
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



async def graph():
    tools = await client.get_tools()

    # Add the local conversion tool
    tools.append(convert_europe_amsterdam_to_unix)

    return create_react_agent(
        name="TransactionsAgent",
        model=llm,
        prompt=PROMPT,
        tools=tools
    )
