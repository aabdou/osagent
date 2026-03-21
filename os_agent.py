from datetime import date, timedelta

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

from tools import make_github_tool, save_to_csv

_since = (date.today() - timedelta(weeks=24)).isoformat()

SYSTEM_PROMPT = f"""
You are a software engineering manager. Your goal is to help boost your team's contributions to open source projects.

The issues you choose must be:
- Opened within the last 24 weeks specifically since {_since}.
- Limited to issues in English and if translation is required to English and Arabic
- The issues must be simple enough for first contributions to open source

The user will provide the name of the repository they want to contrinute to. 

Your tasks are:
1. Query the repository for issues that match the criteria above using the github tool. 
2. Use the save_to_csv tool to save the issues to a CSV file, then print the file path and the issues count
"""


def build_agent():
    model = ChatAnthropic(model="claude-sonnet-4-6")

    return create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[make_github_tool(), save_to_csv],
    )
