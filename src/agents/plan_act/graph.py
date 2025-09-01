import operator
from typing import Annotated, List, Tuple, Union, Literal
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt, ActionRequest
from langgraph.types import interrupt, Command

# Choose the LLM that will drive the agent
llm = AzureChatOpenAI(model="gpt-4.1")
prompt = "You are a helpful assistant."
agent_executor = create_react_agent(llm, [], prompt=prompt)


class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str
    messages: Annotated[list, add_messages]

class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.""",
        ),
        ("placeholder", "{messages}"),
    ]
)
planner = planner_prompt | AzureChatOpenAI(
    model="gpt-4.1", temperature=0

).with_structured_output(Plan)

class Response(BaseModel):
    """Response to user."""

    response: str

class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


replanner_prompt = ChatPromptTemplate.from_template(
    """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
)

replanner = replanner_prompt | AzureChatOpenAI(
    model="gpt-4.1", temperature=0
).with_structured_output(Act)

async def execute_step(state: PlanExecute):
    plan = state["plan"]
    plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
    task = plan[0]
    task_formatted = f"""For the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    agent_response = await agent_executor.ainvoke(
        {"messages": [("user", task_formatted)]}
    )
    return {
        "past_steps": [(task, agent_response["messages"][-1].content)],
    }


async def plan_step(state: PlanExecute):
    state["input"] = state["messages"][-1].content
    plan = await planner.ainvoke({"messages": [("user", state["input"])]})
    return {"plan": plan.steps , "input": state["input"]}


async def replan_step(state: PlanExecute):
    output = await replanner.ainvoke(state)
    if isinstance(output.action, Response):
        return {"response": output.action.response, "messages":[output.action.response]}
    else:
        return {"plan": output.action.steps}


def should_end(state: PlanExecute):
    if "response" in state and state["response"]:
        return END
    else:
        return "agent"

def human_approval(state: PlanExecute) -> Command[Literal["agent", END]]:
    request = HumanInterrupt(
        action_request=ActionRequest(
            action="Approve or Decline",  # The action being requested
            args={"Plan": "\n".join(f"{i + 1}. {step}" for i, step in enumerate(state["plan"])) }  # Arguments for the action
        ),
        config=HumanInterruptConfig(
            allow_ignore=False,    # Allow skipping this step
            allow_respond=False,   # Allow text feedback
            allow_edit=False,     # Don't allow editing
            allow_accept=True     # Allow direct acceptance
        ),
        description="Please review the command before execution"
    )
# Send the interrupt request and get the response
    response = interrupt([request])[0]
    is_approved = response["type"]

    if is_approved:
        return Command(goto="agent")
    else:
        return Command(goto=END)
    
workflow = StateGraph(PlanExecute)

# Add the plan node
workflow.add_node("planner", plan_step)

workflow.add_node("human", human_approval)

# Add the execution step
workflow.add_node("agent", execute_step)

# Add a replan node
workflow.add_node("replan", replan_step)

workflow.add_edge(START, "planner")

# From plan we go to agent
workflow.add_edge("planner", "human")

# From plan we go to agent
workflow.add_edge("human", "agent")

# From agent, we replan
workflow.add_edge("agent", "replan")

# workflow.add_conditional_edges(
#     "human",
#     # Next, we pass in the function that will determine which node is called next.
#     should_end,
#     ["agent", END],
# )

workflow.add_conditional_edges(
    "replan",
    # Next, we pass in the function that will determine which node is called next.
    should_end,
    ["agent", END],
)

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()