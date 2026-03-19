import os
import logging
from github import Github, Auth
from typing import List, Any
from datetime import datetime

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