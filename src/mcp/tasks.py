from typing import List, Optional
from typing import Tuple
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP, Context

# --- MCP Server ---

mcp = FastMCP("Manage customer tasklist API",port=10005)

# Tool for ABN AMRO Get Tasks API (from curl)
@mcp.tool()
def get_tasks(ctx: Context) -> dict:
    """
    Calls the ABN AMRO Get Tasks API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/my-abnamro/apis/bapi/tasks/v2/"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "priority": "u=1, i",
        "origin": "https://www.abnamro.nl",
        "referer": "https://www.abnamro.nl/my-abnamro/tasks/overview/index.html",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-xsrf-header": "token",
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

# Tool for ABN AMRO Delete Task API (from curl)
@mcp.tool()
def delete_task(ctx: Context, task_ids: list[str], source_system: str = "GENERIC_SIGNING") -> dict:
    """
    Calls the ABN AMRO Delete Task API as described in the provided curl request.
    Parameters:
        task_ids: List of task IDs to delete.
        source_system: Source system for the delete operation (default: GENERIC_SIGNING).
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/my-abnamro/apis/bapi/tasks/v2/delete"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    params = {
        "sourceSystem": source_system
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.abnamro.nl",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/tasks/overview/index.html",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-xsrf-header": "token",
        "cookie": cookie
    }

    json_body = {
        "taskIds": task_ids
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=json_body,
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