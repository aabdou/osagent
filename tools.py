import csv
import os
from dataclasses import dataclass
from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import Any, Dict, List, Protocol

from github import Auth, Github
from github.GithubObject import NotSet, Opt
from github.Issue import IssueSearchResult
from github.PaginatedList import PaginatedList

OUTPUT_DIRECTORY = Path("output")


@dataclass
class Result:
    filepath: str
    count: int


class GithubClient(Protocol):
    def search_issues(
        self,
        query: str,
        sort: Opt[str] = NotSet,
        order: Opt[str] = NotSet,
        **qualifiers: Any,
    ) -> PaginatedList[IssueSearchResult]:
        pass


def github_issues(
    repo: str, since: datetime, github_client: GithubClient
) -> List[Dict[str, str]]:
    result = github_client.search_issues(
        f"repo:{repo} is:open is:issue created:>{since}"
    )

    return [{"title": i.title, "url": i.html_url} for i in islice(result, 50)]


def save_to_csv(
    gh_issues: List[Dict[str, str]], output_dir: Path = OUTPUT_DIRECTORY
) -> Result:
    """Save a list of GitHub issues to a CSV file and return the filepath and count"""
    filename = f"issues-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    filepath = output_dir / filename
    with open(filepath, "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([[i["title"], i["url"]] for i in gh_issues])

    return Result(filepath, len(gh_issues))


def make_github_tool():
    github_token = os.getenv("GITHUB_TOKEN")
    auth = Auth.Token(github_token)
    github_client = Github(auth=auth)

    def github_issues_tool(repo: str, since: str) -> List[Dict[str, str]]:
        """
        Fetch repo issues created since the time in the since argument.
        since must be a date string in YYYY-MM-DD format e.g. 2025-09-20
        """
        return github_issues(repo, since, github_client)

    return github_issues_tool
