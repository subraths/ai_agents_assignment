import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def build_chain():
    system_prompt = (
        "You are a virtual interview preparation and assessment agent. "
        "You ask clarifying questions about role, level, and focus area. "
        "Then you conduct a mock interview, give structured feedback, "
        "and provide improvement tips."
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
        temperature=0.3,
    )

    return prompt | llm | StrOutputParser()


def main():
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it in your environment or .env file."
        )

    chain = build_chain()

    print("Virtual Interview Preparation & Assessment Agent")
    print(
        "Example: 'Mock interview for a senior backend engineer role, focus on system design.'"
    )
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in {"exit", "quit"}:
            break

        response = chain.invoke({"user_query": user_query})
        print("\n" + response + "\n")


if __name__ == "__main__":
    main()
