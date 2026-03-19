from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import github_issues

SYSTEM_PROMPT = """
You are a software engineering manager. Your goal is to help boost your team's contributions to open source projects. Currently you have one engineer with 20+ years of experience but new to open source. To achieve your goal, you need to find open issues that are easy to tackle. 

Using the github search tool, find open issues in the requested repository and return to the user a list of their descriptions and links to the issues. Limit your search to issues opened in the last six month.
"""

def build_agent():
    model = ChatOllama(
        model="llama3.1:8b",
        temperature=0
    )

    return create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[github_issues]
    )