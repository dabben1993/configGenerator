import os
from git import Repo
from git.exc import GitCommandError
import structlog

log = structlog.get_logger()


class GitService:
    def __init__(self, repo_url, branch, destination, new_branch_name=None):
        self.new_branch_name = new_branch_name
        self.repo_url = repo_url
        self.branch = branch
        self.repo_name = None
        self.destination = destination
        self.repo = self._clone_repo()

    def _get_repo_name(self):
        try:
            repo_name = self.repo_url.split('/')[-1].split('.')[0]
            log.info("Repo name extraced", repo_name=repo_name)
            return repo_name
        except Exception as e:
            log.warning("Error extracting repo name", error=str(e))
            raise

    def _update_existing_repo(self):
        try:
            repo = Repo(self.destination)
            log.info("Repository exists", repo=self.repo_name, status="Updating...")
            origin = repo.remote(name='origin')
            origin.pull()
            return repo
        except GitCommandError as git_error:
            log.error("Error updating existing repository", error=str(git_error))
            raise
        except Exception as e:
            log.error("Unexpected error during repository update", error=str(e))
            raise

    def _clone_new_repo(self):
        try:
            repo = Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
            log.info("Repository cloned successfully", repo=self.repo_name,
                     url=self.repo_url, branch=self.branch, status="Cloned successfully")
            return repo
        except Exception as e:
            log.warning("Error cloning new repository", error=str(e))
            raise

    def _clone_repo(self):
        try:
            self.repo_name = self._get_repo_name()
            self.destination = os.path.join(self.destination, self.repo_name)

            if os.path.exists(self.destination):
                return self._update_existing_repo()
            else:
                return self._clone_new_repo()
        except Exception as e:
            log.warning("Error cloning repository", error=str(e))
            raise

    def checkout_new_branch(self, branch_name=None):
        try:
            self.repo.git.checkout(b=branch_name)
            log.info("Branch created and checked out", branch_checked_out_from=self.branch,
                     branch_checked_out=branch_name)
        except Exception as e:
            log.warning("Error checking out new branch", error=str(e))
            raise

    def commit_changes(self, commit_message):
        try:
            self.repo.git.add("--all")
            self.repo.index.commit(commit_message)
            log.info("Changes committed", commit_message=commit_message)
        except Exception as e:
            log.warning("Error committing changes", error=str(e))
            raise

    def push_changes(self):
        try:
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.new_branch_name}:{self.new_branch_name}')
            log.info("Changes pushed", pushed_to_branch=self.new_branch_name)
        except GitCommandError as e:
            log.warning("Error pushing changes to the remote repository", error=str(e))
            raise

    def create_and_push_to_new_branch(self, commit_message):
        try:
            self.checkout_new_branch(self.new_branch_name)
            self.commit_changes(commit_message)
            self.push_changes()

        except GitCommandError as e:
            log.warning("Error creating or pushing changes to the new file", error={e})
