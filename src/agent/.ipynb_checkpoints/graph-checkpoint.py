from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from src.agent.device_tools import tools
from src.agent.llm import llm
from src.agent.prompt import prompt_template
from traceloop.sdk.decorators import task, workflow

# 1. Initialize State/Memory
memory = MemorySaver()

# 2. Compile the ReAct Agent
AGENT = create_react_agent(model=llm, tools=tools, state_modifier=prompt_template, checkpointer=memory)


@task()
async def get_ai_response(events):
    # ... (Unchanged logic to extract the final AIMessage with no tool_calls)
    for event in reversed(events):
        if event.get("messages"):
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage) and not last_message.tool_calls:
                try:
                    content = last_message.content
                    # Simplified content handling (keeping it robust)
                    if isinstance(content, str):
                        return content
                    elif isinstance(content, list):
                        # Assuming a flat list of items for simplicity
                        return " ".join([str(item) for item in content])
                    else:
                        return str(content)
                except Exception as e:
                    print(f"Error extracting response: {e}")
                    return "An error occurred while processing the response."

    return None


def print_event(event):
    # ... (Unchanged debug print logic)
    message = event.get("messages", [])
    if message:
        if isinstance(message, list):
            message = message[-1]
        message.pretty_print()  # Commented out as pretty_print requires a dependency


@workflow(name="resmed-support-agent")
async def run_agent(thread_id: str, user_input: str):
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", user_input)]}

    events = []
    # Async stream execution of the agent
    async for event in AGENT.astream(inputs, config=config, stream_mode="values"):
        print_event(event) # Uncomment to see trace logs
        events.append(event)

    response = await get_ai_response(events)
    if response is None:
        response = "An internal error has occurred."
    return {"response": response}