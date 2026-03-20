import os
import logging
import csv
from pathlib import Path
from github import Github, Auth
from typing import List, Any
from datetime import datetime
from dataclasses import dataclass

OUTPUT_DIRECTORY = Path("output")

@dataclass
class Result:
    filepath: str
    count: int

github_token = os.getenv("GITHUB_TOKEN")
auth = Auth.Token(github_token)
g = Github(auth=auth)

def github_issues(repo: str, since: datetime) -> List[Any]:
    """ Fetch repo issues created since the time in the since argument """
    res = []
    try:
        repo = g.get_repo(repo)
        logging.info(f"Connected to: {repo.full_name}")
        
        # List the 5 most recent issues
        for issue in repo.get_issues(state='open', since=since):
            res.append(issue)
            
    except Exception as e:
        logging.error(e)

    return res

def save_to_csv(gh_issues: List[Any], output_dir: Path = OUTPUT_DIRECTORY) -> Result:
    filename = f"issues-{datetime.now().strftime("%Y%m%d_%H%M%S")}"
    filepath = output_dir / filename
    with open(filepath, "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([[i.title, i.url] for i in gh_issues])

    return Result(filepath, len(gh_issues))