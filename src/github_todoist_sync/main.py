# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygithub>=2.5.0",
#     "python-dotenv>=1.0.1", 
#     "todoist-api-python>=2.1.7",
# ]
# ///

from github import Github
from github.PaginatedList import PaginatedList
from github.Issue import Issue
from todoist_api_python.api import TodoistAPI, Task
import os
from dotenv import load_dotenv


class GithubTodoistSyncer:
    def __init__(
        self,
        github_token: str,
        todoist_token: str,
        todoist_project_id: str | None = None,
    ):
        """
        Initialize the sync service with API tokens.

        Args:
            github_token (str): GitHub personal access token
            todoist_token (str): Todoist API token
        """
        self.github = Github(github_token)
        self.todoist = TodoistAPI(todoist_token)
        self.todoist_project_id = todoist_project_id
        self.user = self.github.get_user()
        print(f"Authenticated as GitHub user: {self.user.login}")
        self.tasks = self._get_todoist_tasks()
        print(f"{len(self.tasks)} tasks found in Todoist.")
        self.issues = self._get_assigned_issues()
        print(
            f"{self.issues.totalCount} issues assigned to {self.user.login} found in GitHub."
        )

    def _get_assigned_issues(self) -> PaginatedList[Issue]:
        """
        Get all issues assigned to the authenticated user.

        Returns:
            PaginatedList[Issue]: List of GitHub issues
        """
        query = f"is:issue archived:false assignee:{self.user.login}"
        return self.github.search_issues(query=query)

    def _get_todoist_tasks(self) -> list[Task]:
        """
        Get all tasks from the authenticated Todoist user.

        Returns:
            list: List of Todoist tasks
        """
        return self.todoist.get_tasks()

    def get_task(self, issue: Issue) -> Task | None:
        """
        Returns Todoist task that contains the issue URL, if one exists.

        Args:
            issue (Issue): The GitHub issue to check

        Returns:
            Task or None: The Todoist task, if it exists, otherwise None
        """
        for task in self.tasks:
            if issue.html_url in task.description:
                return task
        return None

    def create_task(self, issue: Issue) -> None:
        """
        Create a Todoist task from a GitHub issue.

        Args:
            issue (Issue): The GitHub issue to create a task for
        """
        # Get task content from issue
        repo = issue.repository.full_name
        title = issue.title
        description = (
            f"GitHub Issue: {issue.html_url}\n\n"
            f"Repository: {repo}\n\n"
            f"Milestone: {issue.milestone.title if issue.milestone else 'No milestone'}\n\n"
            f"{issue.body or 'No description provided.'}"
        )

        self.todoist.add_task(
            content=title,
            project=self.todoist_project_id,
            description=description,
            labels=[repo],
        )

    def close_task(self, task: Task) -> None:
        """
        Close a Todoist task.

        Args:
            task (Task): The Todoist task to close
        """
        self.todoist.close_task(task.id)

    def sync(self):
        """
        Syncs assigned GitHub issues with Todoist tasks.

        Creates a Todoist task for each open, assigned GitHub issue that does not already have a
        corresponding task.

        Closes Todoists tasks for closed GitHub issues.
        """
        for issue in self.issues:
            task = self.get_task(issue)
            status = issue.state
            if task:
                print(f"Task found for issue: {issue.title}")
                if status == "closed":
                    print(f"Closing task for issue: {issue.title}")
                    self.close_task(task)
            else:
                print(f"No task found for issue: {issue.title}")
                if status == "open":
                    print(f"Creating task for issue: {issue.title}")
                    self.create_task(issue)


def main():
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    print(github_token)
    todoist_token = os.getenv("TODOIST_TOKEN")
    todoist_project_id = os.getenv("TODOIST_PROJECT_ID")

    if not github_token or not todoist_token:
        raise ValueError(
            "GITHUB_TOKEN and TODOIST_TOKEN environment variables must be set."
        )
    print("Instantiating syncer...")
    syncer = GithubTodoistSyncer(github_token, todoist_token, todoist_project_id)
    print("Syncing...")
    syncer.sync()


if __name__ == "__main__":
    main()
