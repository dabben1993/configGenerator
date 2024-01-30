import os
from git import Repo, repo
from git.exc import GitCommandError
import structlog

log = structlog.get_logger()


def get_repo_name(repo_url):
    try:
        repo_name = repo_url.split('/')[-1].split('.')[0]
        log.info("Repo name extraced", repo_name=repo_name)
        return repo_name
    except Exception as e:
        log.warning("Error extracting repo name", error=str(e))
        raise


def update_existing_repo(destination, repo_name):
    try:
        repo = Repo(destination)
        log.info("Repository exists", repo=repo_name, status="Updating...")
        origin = repo.remote(name='origin')
        origin.pull()
        return repo
    except GitCommandError as git_error:
        log.error("Error updating existing repository", error=str(git_error))
        raise
    except Exception as e:
        log.error("Unexpected error during repository update", error=str(e))
        raise


def clone_new_repo(repo_url, destination, branch):
    try:
        repo = Repo.clone_from(repo_url, destination, branch=branch)
        log.info("Repository cloned successfully", repo=get_repo_name(repo_url),
                 url=repo_url, branch=branch, status="Cloned successfully")
        return repo
    except Exception as e:
        log.warning("Error cloning new repository", error=str(e))
        raise


def clone_repo(repo_url, destination, branch):
    try:
        repo_name = get_repo_name(repo_url)
        destination = os.path.join(destination, repo_name)

        if os.path.exists(destination):
            return update_existing_repo(repo_name=repo_name, destination=destination)
        else:
            return clone_new_repo(repo_url=repo_url, destination=destination, branch=branch)
    except Exception as e:
        log.warning("Error cloning repository", error=str(e))
        raise


def checkout_new_branch(repository, branch_name=None):
    try:
        checked_out_branch = repository.active_branch.name
        repository.git.checkout(b=branch_name)
        log.info("Branch created and checked out", branch_checked_out_from=checked_out_branch,
                 branch_checked_out=branch_name)
    except Exception as e:
        log.warning("Error checking out new branch", error=str(e))
        raise


def commit_changes(repository, commit_message):
    try:
        repository.git.add("--all")
        repository.index.commit(commit_message)
        log.info("Changes committed", commit_message=commit_message)
    except Exception as e:
        log.warning("Error committing changes", error=str(e))
        raise


def push_changes(repository):
    try:
        origin = repository.remote(name='origin')
        origin.push(refspec=f'{repository.active_branch.name}:{repository.active_branch.name}')
        log.info("Changes pushed", pushed_to_branch=repository.active_branch.name)
    except GitCommandError as e:
        log.warning("Error pushing changes to the remote repository", error=str(e))
        raise


def create_and_push_to_new_branch(repository, new_branch_name, commit_message):
    try:
        checkout_new_branch(repository=repository, branch_name=new_branch_name)
        commit_changes(repository=repository, commit_message=commit_message)
        push_changes(repository=repository)

    except GitCommandError as e:
        log.warning("Error creating or pushing changes to the new file", error={e})


class GitService:
    def __init__(self, PAT=None, user_name=None, password=None):
        self.pat = PAT
        self.user_name = user_name
        self.password = password
