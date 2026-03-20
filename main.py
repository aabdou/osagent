from dotenv import load_dotenv
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()
from os_agent import build_agent

def main():
    agent = build_agent()
    response = agent.invoke({"messages": HumanMessage("I want to contribute to fastapi/fastapi.")})
    for message in response['messages']:
        pprint(message)
    gh_list = response.get("structured_response")

if __name__ == "__main__":
    main()
