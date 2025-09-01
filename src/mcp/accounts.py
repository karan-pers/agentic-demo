from typing import List, Optional, Literal
from typing import Tuple
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP, Context

class Balance(BaseModel):
    amount: float
    spendingBalance: float
    sumOfReservations: float
    currencyCode: str

class Product(BaseModel):
    resourceType: str
    buildingBlockId: int
    name: str
    productGroup: str
    id: int
    internalProductName: str
    creditAccount: bool

class Customer(BaseModel):
    bcNumber: int

class Contract(BaseModel):
    accountNumber: str
    resourceType: str
    id: str
    contractNumber: str
    chid: Optional[str] = None
    status: str
    balance: Balance
    product: Product
    customer: Customer
    isBlocked: bool

class ContractWrapper(BaseModel):
    contract: Contract

class ContractList(BaseModel):
    contractList: List[ContractWrapper]

mcp = FastMCP("Account Balance API", port=10000)

common_headers = {
    "accept": "application/json",
    "accept-language": "en",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Referer": "https://www.abnamro.nl/my-abnamro/my-overview/overview/index.html",
    "origin": "https://www.abnamro.nl",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

@mcp.tool()
def get_account_balance_list(ctx: Context) -> Tuple[str, ContractList]:
    """
    Calls the Account Balance API as described in the OpenAPI spec.
    """
    # Compose the endpoint (using PR server as in sample curl)
    url = "https://www.abnamro.nl/my-abnamro/apis/account-balances/v2/"

    cookie = ctx.request_context.request.headers.get("cookie", "")

    # Compose query parameters (match curl sample)
    params = {
        "productGroups": ["PAYMENT_ACCOUNTS","SAVINGS_ACCOUNTS","INVESTMENTS","FISCAL_CAPITAL_SOLUTIONS","FISCAL_CAPITAL_SOLUTIONS_PRODUCTS","MORTGAGE","DEPOSITS"],
        "excludeBlocked": False
    }

    req_headers = {
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|d411be3b67b44b35a9dc91bf4f1e1a1e.05b76be958b74dfe",
        "source": "aab-sys-020419",
        "traceparent": "00-d411be3b67b44b35a9dc91bf4f1e1a1e-05b76be958b74dfe-01",
        "x-xsrf-header": "token",
    }

    headers = {**common_headers, **req_headers , "cookie": cookie}
    
    # Make the HTTP GET request with a timeout to prevent hanging indefinitely
    response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    data = response.json()
    print("Response data:", data)
    # Parse the response into ContractList
    contract_list = ContractList.model_validate(data)

    # Compose a human-readable summary for unstructured output
    summary = f"Accounts found: {len(contract_list.contractList)}. "
    if contract_list.contractList:
        first = contract_list.contractList[0].contract
        summary += f"First account: {first.accountNumber} ({first.product.name}), Balance: {first.balance.amount} {first.balance.currencyCode}."

    # Return both structured and unstructured output as a tuple (per MCP SDK structured output docs)
    return summary, contract_list

@mcp.tool(
    description="This tool fetches the list of accounts for the ABN AMRO user. The main account is called 'Personal Account'.",
)
def get_payments_contracts_list(ctx: Context) -> dict:
    """
    Calls the ABN AMRO Payments Contracts List API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/my-abnamro/api/payments/contracts/list"

    cookie = ctx.request_context.request.headers.get("cookie", "")

    data = {
        "actionNames": [
            "VIEW_PORTFOLIO_OVERVIEW", "VIEW_PAYMENTS", "APM_ADVISE_CONTRACTFILTER",
            "MANAGE_DOMESTIC_PAYMENTS", "MANAGE_INTERNATIONAL_PAYMENTS", "SIGN_DOMESTIC_PAYMENTS",
            "SIGN_INTERNATIONAL_PAYMENTS", "SIGN_STANDING_ORDER", "VIEW_PROFILE_FUND_SETTINGS",
            "VIEW_WEALTH_OVERVIEW"
        ],
        "productBuildingBlocks": [5, 8, 20, 25, 15],
        "productGroups": [
            "PAYMENT_ACCOUNTS", "SAVINGS_ACCOUNTS", "INVESTMENTS",
            "FISCAL_CAPITAL_SOLUTIONS", "FISCAL_CAPITAL_SOLUTIONS_PRODUCTS", "MORTGAGE"
        ],
        "balanceTypes": ["IBMR", "ITBD"],
        "excludeBlocked": False,
        "contractIds": []
    }

    req_headers = {
        "consumer-id": "aabsys020419-retail-digitalshop",
        "content-type": "application/json"
    }

    headers = {**common_headers, **req_headers , "cookie": cookie}

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=10,
        verify=False
    )
    try:
        resp_json = response.json()
    except Exception as e:
        print("Failed to parse JSON response:", e)
        resp_json = {"error": str(e), "text": response.text}
    return resp_json


# Tool for ABN AMRO Get Transactions API (from curl)
@mcp.tool()
def get_transactions(
    ctx: Context,
    account_number: str,
    last_mutation_key: Optional[str] = None,
    include_actions: str = "EXTENDED",
    transaction_type: Optional[Literal['CREDIT', 'DEBIT']] = None,
    book_date_from: Optional[int] = None,
    book_date_to: Optional[int] = None
) -> dict:
    """
    Calls the ABN AMRO Get Transactions API as described in the provided curl request.
    transaction_type: Optional enum, one of 'CREDIT' or 'DEBIT'.
    book_date_from: Optional[int], timestamp(in milliseconds) for the start date (at time 00:00:00) of transactions.
    book_date_to: Optional[int], timestamp(in milliseconds) for the end date (at time 00:00:00) of transactions.
    Returns the JSON response as a dict.
    """
    url = f"https://www.abnamro.nl/mutations/{account_number}"

    # Extract cookie from context headers
    cookie = ctx.request_context.request.headers.get("cookie", "")

    params = {
        "accountNumber": account_number,
        "includeActions": include_actions,
        "lastMutationKey": last_mutation_key,
        "cdIndicatorAmountFrom": transaction_type,
        "cdIndicatorAmountTo": transaction_type,
        "bookDateFrom": book_date_from,
        "bookDateTo": book_date_to
    }
    # Remove keys with None values
    params = {k: v for k, v in params.items() if v is not None}

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/transactions/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|a597dd2fdd9f4f3798e56b6b26c73c5d.76d2c0c4ff55497a",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-a597dd2fdd9f4f3798e56b6b26c73c5d-76d2c0c4ff55497a-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-aab-serviceversion": "v3",
        "cookie": cookie
    }

    response = requests.get(
        url,
        params=params,
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
    print("Starting MCP server...")
    mcp.run(transport="streamable-http")

