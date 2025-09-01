from typing import List, Optional
from typing import Tuple
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP, Context

# --- MCP Server ---

mcp = FastMCP("Manage customer or user preferences API",port=10004)

# Tool for ABN AMRO Get Newsletter Settings API (from curl)
@mcp.tool()
def get_newsletter_settings(
    ctx: Context,
    bcnumber: str,
    cgc_code:str = "0213",
) -> dict:
    """
    Calls the ABN AMRO Get Newsletter Settings API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/customer-communication-preferences/v1/newsletters?cgcCode={cgc_code}"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "bcnumber": bcnumber,
        "priority": "u=1, i",
        "origin": "https://www.abnamro.nl",
        "referer": "https://www.abnamro.nl/my-abnamro/settings/communication/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|ae1afa10785d41ae9d7beb236c63ac96.9f4f082e377749cd",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-ae1afa10785d41ae9d7beb236c63ac96-9f4f082e377749cd-01",
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
