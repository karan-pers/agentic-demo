from typing import List, Optional
from typing import Tuple
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP, Context

# --- MCP Server ---

mcp = FastMCP("Manage Customer Data API",port=10002)

# Tool for ABN AMRO Manage Data Client API (from curl)
@mcp.tool(
    description="Fetches the details of the customer. This includes name, date of birth, address, email, phone numbers, BSN and other personal information."
)
def get_manage_data_client(ctx: Context) -> dict:
    """
    Calls the ABN AMRO Manage Data Client API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/my-abnamro/manage-data/api/clients/v2/9999"

    # Use the x-forwarded-access-token header as a cookie string, as in other tools
    cookie = ctx.request_context.request.headers.get("cookie", "")

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "mcd-consumer-id": "AAB.SYS.021585",
        "pii-user-id": "2021592065",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/manage-data/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|7066723da1534efea831c5ae6d33f869.cefa6a445da24892",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": cookie,
        "traceparent": "00-7066723da1534efea831c5ae6d33f869-cefa6a445da24892-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
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

# Tool for ABN AMRO Validate New Phone Number API (from curl)
@mcp.tool(
    description="Validates a new phone number for a customer"
)
def validate_new_phone_number(
    ctx: Context,
    international_calling_code: str,
    new_phone_number: str,
    user_id: str
) -> dict:
    """
    Calls the ABN AMRO Validate New Phone Number API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/my-abnamro/manage-data/api/phonenumbers/v1?userIdType=CUSTOMER_ID"

    # Use the x-forwarded-access-token header as a cookie string, as in other tools
    cookie = ctx.request_context.request.headers.get("cookie", "")

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "content-type": "application/json",
        "mcd-consumer-id": "AAB.SYS.021585",
        "pii-international-calling-code": international_calling_code,
        "pii-organization-unit-id": "695221",
        "pii-phone-number": new_phone_number,
        "pii-user-id": user_id,
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/manage-data/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|b41030fe589840319cfa8d1b540e366f.c08fdd6e5b4144ab",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": cookie,
        "traceparent": "00-b41030fe589840319cfa8d1b540e366f-c08fdd6e5b4144ab-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
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

# Tool for ABN AMRO Change Phone Number API (from curl)
@mcp.tool(
    description="Submits a phone number change request for a customer"
)
def change_phone_number(
    ctx: Context,
    business_contact_number: int = 2021592065,
    international_calling_code: int = 31,
    phone_number: str = "651207540",
    formatted_phone_number: str = "+31 6 51207540",
    country_code: str = "NL",
    client_type: str = "PRIVATE_BUSINESS_CONTACT"
) -> dict:
    """
    Calls the ABN AMRO Change Phone Number API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/my-abnamro/apis/pact/individual-party-phone-update-requests/v1/"

    # Extract cookie from context headers
    cookie = ctx.request_context.request.headers.get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.abnamro.nl",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/manage-data/index.html",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|b41030fe589840319cfa8d1b540e366f.45d250bd01e0436c",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-b41030fe589840319cfa8d1b540e366f-45d250bd01e0436c-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-xsrf-header": "token",
        "cookie": cookie
    }

    body = {
        "subjectBusinessContacts": [
            {
                "clientType": client_type,
                "businessContactNumber": business_contact_number,
                "phoneNumbers": {
                    "landLinePhoneNumbers": [
                        {"formattedPhoneNumber": ""}
                    ],
                    "mobilePhoneNumbers": [
                        {
                            "country": {"countryCode": country_code},
                            "internationalCallingCode": international_calling_code,
                            "phoneNumber": phone_number,
                            "formattedPhoneNumber": formatted_phone_number
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(
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


# Tool for ABN AMRO Customer Representatives API (from curl)
@mcp.tool(
    description="Fetches business contacts list for the customer.This includes details like bcNumber, shortName, serviceSegment, clientGroupCode(cgc) and appearanceType"
)
def customer_representatives(ctx: Context) -> dict:
    """
    Calls the ABN AMRO Customer Representatives API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/representatives/representative/customers/v4"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/transactions/",
        "request-context": "appId=cid-v1:713be00b-c043-46c7-8dbc-9ab5de899aad",
        "request-id": "|a597dd2fdd9f4f3798e56b6b26c73c5d.24bb9d4e79c647c0",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-a597dd2fdd9f4f3798e56b6b26c73c5d-24bb9d4e79c647c0-01",
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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")



