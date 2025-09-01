from typing import List, Optional
from typing import Tuple
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP, Context

# --- MCP Server ---

mcp = FastMCP("Customer/User Message management API",port=10003)

# Tool for ABN AMRO Get Messages API (from curl)
@mcp.tool()
def get_messsages(ctx: Context) -> dict:
    """
    Calls the ABN AMRO Get Messages API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/my-abnamro/api/message-card/v1/message-cards"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/tasks/overview/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|2f7c58e965ab4ee696f0ffe4bf6d16fc.9be044f080384c21",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-2f7c58e965ab4ee696f0ffe4bf6d16fc-9be044f080384c21-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        verify=False
    )
    try:
        resp_json = response.json()
    except Exception as e:
        print("Failed to parse JSON response:", e)
        resp_json = {"error": str(e), "text": response.text}
    return resp_json

# Tool for ABN AMRO Delete Message API (from curl)
@mcp.tool()
def delete_message(
    ctx: Context,
    message_id: int,
    is_bankmail: bool = False
) -> dict:
    """
    Calls the ABN AMRO Delete Message API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/my-abnamro/api/message-card/v1/message-cards/{message_id}/status?isBankmail={'true' if is_bankmail else 'false'}"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.abnamro.nl",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/tasks/overview/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|2f7c58e965ab4ee696f0ffe4bf6d16fc.397152556f1f4600",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-2f7c58e965ab4ee696f0ffe4bf6d16fc-397152556f1f4600-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    body = {"status": "DELETE"}

    response = requests.put(
        url,
        headers=headers,
        json=body,
        timeout=10,
        verify=False
    )
    try:
        resp_json = response.json()
    except Exception as e:
        print("Failed to parse JSON response:", e)
        resp_json = {"error": str(e), "text": response.text}
    return resp_json


# Tool for ABN AMRO Read Message API (from curl)
@mcp.tool()
def get_detailed_message(
    ctx: Context,
    message_card_id: int,
    expanded_card_id: int,
    is_bankmail: bool = False
) -> dict:
    """
    Calls the ABN AMRO Read Message API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/my-abnamro/api/message-card/v1/message-cards/{message_card_id}/expanded-cards/{expanded_card_id}?isBankmail={'true' if is_bankmail else 'false'}"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/self-service/overview/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|7883902029bf4df1ae2ab4ea49b6339e.1b95a6d011ca4bf1",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-7883902029bf4df1ae2ab4ea49b6339e-1b95a6d011ca4bf1-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        verify=False
    )
    try:
        resp_json = response.json()
    except Exception as e:
        print("Failed to parse JSON response:", e)
        resp_json = {"error": str(e), "text": response.text}
    return resp_json
# --- MCP Server ---

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

