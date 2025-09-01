from typing import Optional
import requests
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("Address Book API", port=10001)

@mcp.tool(
    description="Fetches the payments address book for a customer"
)
def fetch_address_book(
    ctx: Context,
    owner_reference: str,
    owner_class: str = "BUSINESS_CONTACT",
    include_total_number_of_elements: bool = True,
    page_number: int = 1,
    page_size: int = 100,
    search_string: str = "",
    timestamp: Optional[int] = None
) -> dict:
    """
    Calls the ABN AMRO Address Book API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/paymentmodels"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}) .get("cookie", "")

    params = {
        "ownerClass": owner_class,
        "ownerReference": owner_reference,
        "includeTotalNumberOfElements": str(include_total_number_of_elements).lower(),
        "pageNumber": page_number,
        "pageSize": page_size,
        "searchString": search_string,
        "timestamp": timestamp
    }
    # Remove keys with None values
    params = {k: v for k, v in params.items() if v is not None}

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|8b6ceb9d09ad4d9bb050e966f25c200f.ec5065402d844b89",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-8b6ceb9d09ad4d9bb050e966f25c200f-ec5065402d844b89-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-aab-serviceversion": "v2",
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

@mcp.tool(
    description="Fetches payment account number formats for a given country and currency"
)
def fetch_account_number_formats(
    ctx: Context,
    country_iso_codes: str = "NL",
    currency_iso_code: str = "EUR"
) -> dict:
    """
    Calls the ABN AMRO Payment Account Number Formats API as described in the provided curl request.
    Returns the JSON response as a dict.
    """
    url = "https://www.abnamro.nl/paymentaccountnumberformats"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    params = {
        "countryIsoCodes": country_iso_codes,
        "currencyIsoCode": currency_iso_code
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|4c3ac2b5a7794523ad0c4f2f6dc8e0b2.50f3324fe5c740e8",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-4c3ac2b5a7794523ad0c4f2f6dc8e0b2-50f3324fe5c740e8-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
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

@mcp.tool(
    description="Creates a single SEPA payment request for executing a payment or transaction"
)
def fetch_single_sepa_payment_instruction(
    ctx: Context,
    ordering_party_name: str,
    ordering_account_number: str,
    contract_number: str,
    business_contact_number: int,
    transaction_account_number: str,
    transaction_counter_party_name: str,
    transaction_amount: str,
    ordering_party_type: str = "DEBTOR",
    ordering_account_currency: str = "EUR",
    building_block_id: int = 5,
    transaction_counter_party_type: str = "CREDITOR",
    transaction_currency_iso_code: str = "EUR",
    transaction_indication_urgent: bool = False,
    transaction_indication_immediate: bool = True,
    transaction_remittance_info: str = "",
    transaction_remittance_info_type: str = "UNSTRUCTURED",
    support_fraud_message: bool = True,
    payment_continue: bool = False
) -> dict:
    """
    Calls the ABN AMRO Single SEPA Payment Instruction API as described in the provided curl request.
    Returns the JSON response as a dict.
    Parameters are mapped to the JSON body and query string as in the curl.
    """
    url = "https://www.abnamro.nl/my-abnamro/api/payments/paymentinstructions/single/sepa"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    params = {
        "supportFraudMessage": str(support_fraud_message).lower(),
        "paymentContinue": str(payment_continue).lower()
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "content-type": "application/json",
        "origin": "https://www.abnamro.nl",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|32331f0bfd644ab6afabb1673840c59a.f1cb784942ef4ad6",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-32331f0bfd644ab6afabb1673840c59a-f1cb784942ef4ad6-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-aab-serviceversion": "v3",
        "cookie": cookie
    }

    json_body = {
        "sepaPaymentInstruction": {
            "orderingParties": [
                {
                    "type": ordering_party_type,
                    "name": ordering_party_name
                }
            ],
            "accountNumber": ordering_account_number,
            "accountCurrency": ordering_account_currency,
            "buildingBlockId": building_block_id,
            "contractNumber": contract_number,
            "businessContactNumber": business_contact_number,
            "@resourceType": "SepaCreditTransferPaymentInstruction",
            "paymentInstructionTransactionPart": {
                "@resourceType": "SepaPaymentInstructionTransactionPart",
                "accountNumber": transaction_account_number,
                "counterParties": [
                    {
                        "type": transaction_counter_party_type,
                        "name": transaction_counter_party_name
                    }
                ],
                "currencyIsoCode": transaction_currency_iso_code,
                "indicationUrgent": transaction_indication_urgent,
                "amount": transaction_amount,
                "indicationImmediate": transaction_indication_immediate,
                "remittanceInfo": transaction_remittance_info,
                "remittanceInfoType": transaction_remittance_info_type
            }
        }
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

# --- New MCP Tool: fetch_payment_models_query ---
@mcp.tool(
    description="Fetches payment models using the /paymentmodels endpoint with query parameters."
)
def fetch_payment_models_query(
    ctx: Context,
    owner_class: str = "BUSINESS_CONTACT",
    owner_reference: str = "2021592065",
    include_total_number_of_elements: bool = True,
    page_number: int = 1,
    page_size: int = 100,
    search_string: str = "",
    timestamp: int = 1756140737799
) -> dict:
    """
    Calls the ABN AMRO Payment Models API as described in the provided curl request.
    Returns the JSON response as a dict.
    Parameters:
        owner_class: The owner class (default: BUSINESS_CONTACT)
        owner_reference: The owner reference 
        include_total_number_of_elements: Whether to include total number of elements (default: True)
        page_number: Page number (default: 1)
        page_size: Page size (default: 100)
        search_string: Search string (default: empty)
        timestamp: Timestamp for the query
    """
    url = "https://www.abnamro.nl/paymentmodels"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    params = {
        "ownerClass": owner_class,
        "ownerReference": owner_reference,
        "includeTotalNumberOfElements": str(include_total_number_of_elements).lower(),
        "pageNumber": page_number,
        "pageSize": page_size,
        "searchString": search_string,
        "timestamp": timestamp
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|32331f0bfd644ab6afabb1673840c59a.865910a4889544f9",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-32331f0bfd644ab6afabb1673840c59a-865910a4889544f9-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-aab-serviceversion": "v2",
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

@mcp.tool(
    description="Fetches payment instruction type options using the /paymentinstructiontypeoptions endpoint."
)
def fetch_payment_instruction_type_options(
    ctx: Context,
    counter_account_number: str,
    ordering_account_number: str,
    indication_geoblock_blacklist_check: bool = True,
    counter_account_format: str = "IBAN",
    counter_bank_country_iso_code: str = "NL",
    ordering_account_currency_iso_code: str = "EUR",
    transaction_currency_iso_code: str = "EUR"
) -> dict:
    """
    Calls the ABN AMRO Payment Instruction Type Options API as described in the provided curl request.
    Returns the JSON response as a dict.
    Parameters:
        indication_geoblock_blacklist_check: Whether to check geoblock blacklist (default: True)
        counter_account_format: Format of the counter account (default: IBAN)
        counter_account_number: Counter account number
        counter_bank_country_iso_code: Country ISO code of the counter bank (default: NL)
        ordering_account_currency_iso_code: Currency ISO code of the ordering account (default: EUR)
        ordering_account_number: Ordering account number
        transaction_currency_iso_code: Transaction currency ISO code (default: EUR)
    """
    url = "https://www.abnamro.nl/paymentinstructiontypeoptions"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    params = {
        "indicationGeoblockBlacklistCheck": str(indication_geoblock_blacklist_check).lower(),
        "counterAccountFormat": counter_account_format,
        "counterAccountNumber": counter_account_number,
        "counterBankCountryIsoCode": counter_bank_country_iso_code,
        "orderingAccountCurrencyIsoCode": ordering_account_currency_iso_code,
        "orderingAccountNumber": ordering_account_number,
        "transactionCurrencyIsoCode": transaction_currency_iso_code
    }

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|32331f0bfd644ab6afabb1673840c59a.1ad36f44800c4eb3",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-32331f0bfd644ab6afabb1673840c59a-1ad36f44800c4eb3-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
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


@mcp.tool(
    description="Validates a payment account holder using name and IBAN"
)
def fetch_account_holder_validation(
    ctx: Context,
    name: str = "Jonice Siems",
    iban: str = "NL47ABNA0621915505"
) -> dict:
    """
    Calls the ABN AMRO Payment Account Holder Validation API as described in the provided curl request.
    Returns the JSON response as a dict.
    Parameters:
        name: The name of the account holder to validate.
        iban: The IBAN of the account holder to validate.
    """
    url = "https://www.abnamro.nl/paymentaccountholdervalidation"

    # Extract cookie from context headers
    cookie = getattr(getattr(getattr(ctx, "request_context", None), "request", None), "headers", {}).get("cookie", "")

    headers = {
        "accept": "application/json",
        "accept-language": "en",
        "content-type": "application/json",
        "origin": "https://www.abnamro.nl",
        "priority": "u=1, i",
        "referer": "https://www.abnamro.nl/my-abnamro/payments/account/",
        "request-context": "appId=cid-v1:057612d6-4c2a-44a6-ae00-fa8e05bcafeb",
        "request-id": "|4c3ac2b5a7794523ad0c4f2f6dc8e0b2.33cfb8bb609d4bf0",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-4c3ac2b5a7794523ad0c4f2f6dc8e0b2-33cfb8bb609d4bf0-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": cookie
    }

    json_body = {
        "paymentaccountholder": {
            "name": name,
            "iban": iban
        }
    }

    response = requests.post(
        url,
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

if __name__ == "__main__":
    mcp.run(transport="streamable-http")