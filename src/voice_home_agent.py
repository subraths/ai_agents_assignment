import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.devices import turn_on, turn_off, set_value, get_status


def build_chain():
    system_prompt = (
        "You are a voice-controlled home automation AI agent. "
        "You must respond ONLY in this format:\n"
        "ACTION;DEVICE;ROOM(optional);VALUE(optional)\n"
        "Valid ACTION values: ON, OFF, SET, STATUS\n"
        "Examples:\n"
        "ON;lights;living room;\n"
        "OFF;fan;bedroom;\n"
        "SET;thermostat;hallway;22\n"
        "STATUS;lights;living room;\n"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{user_query}"),
        ]
    )

    llm = ChatOpenRouter(
        model="openai/gpt-oss-120b:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.2,
    )

    return prompt | llm | StrOutputParser()


def execute_command(command: str) -> str:
    parts = [p.strip() for p in command.split(";")]
    action = (parts[0] if len(parts) > 0 else "").upper()
    device = parts[1] if len(parts) > 1 else ""
    room = parts[2] if len(parts) > 2 and parts[2] else None
    value = parts[3] if len(parts) > 3 and parts[3] else None

    if action == "ON":
        return turn_on(device, room)
    if action == "OFF":
        return turn_off(device, room)
    if action == "SET":
        if value is None:
            return "[MOCK] Missing value for SET action."
        return set_value(device, value, room)
    if action == "STATUS":
        return get_status(device, room)

    return "[MOCK] Unrecognized command."


def main():
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it in your environment or .env file."
        )

    chain = build_chain()

    print("Voice-Controlled Home Automation AI Agent (Mock Actions + Memory)")
    print("Example: 'Turn off the living room lights and set the thermostat to 22.'")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in {"exit", "quit"}:
            break

        command = chain.invoke({"user_query": user_query})
        result = execute_command(command)

        print("\nCommand:", command)
        print(result + "\n")


if __name__ == "__main__":
    main()
