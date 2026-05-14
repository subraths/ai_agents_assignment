import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from devices import turn_on, turn_off, set_value, get_status

MODEL = "openai/gpt-oss-120b:free"


@tool
def device_on(device: str, room: str = "") -> str:
    """Turn on a device in an optional room."""
    return turn_on(device, room or None)


@tool
def device_off(device: str, room: str = "") -> str:
    """Turn off a device in an optional room."""
    return turn_off(device, room or None)


@tool
def device_set(device: str, value: str, room: str = "") -> str:
    """Set a device value (e.g., thermostat) in an optional room."""
    return set_value(device, value, room or None)


@tool
def device_status(device: str, room: str = "") -> str:
    """Get current device status in an optional room."""
    return get_status(device, room or None)


def build_agent():
    llm = ChatOpenRouter(
        model="openai/gpt-oss-120b:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.2,
    )

    tools = [device_on, device_off, device_set, device_status]

    system_prompt = (
        "You are a voice-controlled home automation AI agent. "
        "Use the tools to control devices. "
        "Ask a short clarification if device or room is ambiguous."
    )

    memory = InMemorySaver()
    agent = create_agent(
        model=MODEL,
        llm=llm,
        tools=tools,
        state_modifier=system_prompt,
        checkpointer=memory,
    )
    return agent


def main():
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it in your environment or .env file."
        )

    agent = build_agent()
    thread_id = "home-session"

    print("Voice-Controlled Home Automation AI Agent (LangGraph + Memory)")
    print("Example: 'Turn on the living room lights.'")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in {"exit", "quit"}:
            break

        result = agent.invoke(
            {"messages": [("user", user_query)]},
            config={"configurable": {"thread_id": thread_id}},
        )

        # Last assistant message
        messages = result["messages"]
        print("\n" + messages[-1].content + "\n")


if __name__ == "__main__":
    main()
