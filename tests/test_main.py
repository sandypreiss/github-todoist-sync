import pytest

from github_todoist_sync.main import GithubTodoistSyncer


@pytest.fixture
def open_issue(mocker):
    issue = mocker.Mock()
    issue.title = "Open Issue"
    issue.html_url = "https://github.com/test/repo/issues/1"
    issue.state = "open"
    issue.repository.full_name = "test/repo"
    issue.milestone = None
    issue.body = "Test description"
    return issue


@pytest.fixture
def closed_issue(mocker):
    issue = mocker.Mock()
    issue.title = "Closed Issue"
    issue.html_url = "https://github.com/test/repo/issues/2"
    issue.state = "closed"
    issue.repository.full_name = "test/repo"
    issue.milestone = None
    issue.body = "Test description"
    return issue


@pytest.fixture
def existing_task(mocker):
    task = mocker.Mock()
    task.id = "task123"
    task.description = "GitHub Issue: https://github.com/test/repo/issues/2"
    return task


@pytest.fixture
def syncer(mocker):
    mocker.patch("github_todoist_sync.main.Github")
    mocker.patch("github_todoist_sync.main.TodoistAPI")

    syncer = GithubTodoistSyncer("github_token", "todoist_token", "project_123")
    return syncer


def test_sync_creates_task_for_open_issue(syncer, open_issue):
    """Test that sync creates a new task for an open issue without existing task"""
    syncer.issues = [open_issue]
    syncer.tasks = []  # No existing tasks

    syncer.sync()

    # Should create a new task for the open issue
    syncer.todoist.add_task.assert_called_once_with(
        content="Open Issue",
        project="project_123",
        description=f"GitHub Issue: {open_issue.html_url}\n\nRepository: test/repo\n\nMilestone: No milestone\n\nTest description",
        labels=["test/repo"],
    )


def test_sync_closes_task_for_closed_issue(syncer, closed_issue, existing_task):
    """Test that sync closes an existing task when its corresponding issue is closed"""
    syncer.issues = [closed_issue]
    syncer.tasks = [existing_task]

    syncer.sync()

    # Should close the existing task
    syncer.todoist.close_task.assert_called_once_with("task123")
