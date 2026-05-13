import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def build_chain():
    system_prompt = (
        "You are an expert AI tourist guide and travel planner."
        "You ask clarifying questions when needed and then produce a concise, "
        "day-by-day itinerary with logistics, budget tips, and local etiquette."
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
        temperature=0.4,
    )

    return prompt | llm | StrOutputParser()


def main():
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Set it in your environment or .env file."
        )

    chain = build_chain()

    print("AI Tourist Guide & Travel Planner")
    print(
        "Type your travel request. Example: 'Plan a 3-day trip to Kyoto in October with a mid-range budget.'"
    )
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in {"exit", "quit"}:
            break

        print("Generating itinerary...")

        response = chain.invoke({"user_query": user_query})
        print("\n" + response + "\n")


if __name__ == "__main__":
    main()
