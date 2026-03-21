from pprint import pprint

from dotenv import load_dotenv
from langchain.messages import HumanMessage

from os_agent import build_agent

load_dotenv()


def main():
    agent = build_agent()
    response = agent.invoke(
        {"messages": HumanMessage("I want to contribute to fastapi/fastapi.")}
    )
    for message in response["messages"]:
        pprint(message)


if __name__ == "__main__":
    main()
