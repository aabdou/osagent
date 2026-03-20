from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools import github_issues
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic

SYSTEM_PROMPT = """
You are a software engineering manager. Your goal is to help boost your team's contributions to open source projects. Currently you have one engineer with 20+ years of experience but new to open source. To achieve your goal, you need to find open issues that are easy to tackle. 

When the user provides a repository, immediately call the github search tool without asking for confirmation and return the list of issues to the user. Limit your search to issues opened in the last six month.
"""

class GithubIssue(BaseModel):
    url: str = Field(min_length=1)
    title: str = Field(min_length=1)

class GithubIssueList(BaseModel):
    issues: list[GithubIssue]

def build_agent():
    model = ChatAnthropic(
        model="claude-sonnet-4-6"
    )

    return create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[github_issues],
        response_format=GithubIssueList
    )