import os
from dotenv import load_dotenv
import logging
import asyncio
import webbrowser
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage
from msal import PublicClientApplication

from microsoft.agents.activity import ActivityTypes
from microsoft.agents.copilotstudio.client import (
    ConnectionSettings,
    CopilotClient,
)

from src.utils.local_toke_cache import LocalTokenCache
ms_agents_logger = logging.getLogger("microsoft.agents")
ms_agents_logger.addHandler(logging.StreamHandler())
ms_agents_logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

TOKEN_CACHE = LocalTokenCache("./.local_token_cache.json")


def acquire_token(settings: ConnectionSettings, app_client_id, tenant_id):
    pca = PublicClientApplication(
        client_id=app_client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        token_cache=TOKEN_CACHE,
    )

    token_request = {
        "scopes": ["https://api.powerplatform.com/.default"],
    }
    accounts = pca.get_accounts()
    retry_interactive = False
    token = None
    try:
        if accounts:
            response = pca.acquire_token_silent(
                token_request["scopes"], account=accounts[0]
            )
            token = response.get("access_token")
        else:
            retry_interactive = True
    except Exception as e:
        retry_interactive = True
        logger.error(
            f"Error acquiring token silently: {e}. Going to attempt interactive login."
        )

    if retry_interactive:
        logger.debug("Attempting interactive login...")
        response = pca.acquire_token_interactive(**token_request)
        token = response.get("access_token")

    return token


async def copilotstudio_agent_node(state: MessagesState):
    if CopilotClient is None:
        raise ImportError(
            "copilotstudio-client is not installed. Run 'pip install copilotstudio-client'.")
    user_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    print("User messages (Human only):", user_messages)
    question = user_messages[-1].content[-1]["text"] if user_messages else ""
    print("question: ", question)
    settings = ConnectionSettings(
        environment_id=os.getenv("COPILOTSTUDIOAGENT__ENVIRONMENTID", ""),
        agent_identifier=os.getenv("COPILOTSTUDIOAGENT__SCHEMANAME", ""),
        cloud=None,
        copilot_agent_type=None,
        custom_power_platform_cloud=None,
    )
    # token = os.getenv("COPILOTSTUDIOAGENT__TOKEN","")
    token = acquire_token(
        settings,
        app_client_id=os.getenv("COPILOTSTUDIOAGENT__AGENTAPPID"),
        tenant_id=os.getenv("COPILOTSTUDIOAGENT__TENANTID"),
    )
    print("Token:", token)
    print("Settings:", settings)
    client = CopilotClient(settings, token)
    act = client.start_conversation(True)
    print("\nSuggested Actions: ")
    async for action in act:
        if action.text:
            print(action.text)
    # Send the message and get the response
    replies = client.ask_question(question, action.conversation.id)
    final_reply = ""
    async for reply in replies:
        if reply.type == ActivityTypes.message:
            print(f"\n{reply.text}")
            final_reply = final_reply + f"\n{reply.text}"
            if reply.suggested_actions:
                for action in reply.suggested_actions.actions:
                    print(f" - {action.title}")
    print("Response:", replies)
    return {"messages": [AIMessage(
        content=final_reply,
        name="copilotstudio_agent"
    )]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("copilotstudio_agent", copilotstudio_agent_node)
graph_builder.add_edge(START, "copilotstudio_agent")
graph_builder.add_edge("copilotstudio_agent", END)

graph = graph_builder.compile(name="KnowledgeAgent")
