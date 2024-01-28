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
        repo_name = self.repo_url.split('/')[-1].split('.')[0]
        log.info("Repo name extraced", repo_name=repo_name)
        return repo_name

    def _update_existing_repo(self):
        repo = Repo(self.destination)
        log.info("Repository exists", repo=self.repo_name, status="Updating...")
        origin = repo.remote(name='origin')
        origin.pull()
        return repo

    def _clone_new_repo(self):
        repo = Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
        log.info("Repository cloned successfully", repo=self.repo_name,
                 url=self.repo_url, branch=self.branch, status="Cloned successfuly")
        return repo

    def _clone_repo(self):
        self.repo_name = self._get_repo_name()
        self.destination = os.path.join(self.destination, self.repo_name)

        if os.path.exists(self.destination):
            return self._update_existing_repo()
        else:
            return self._clone_new_repo()

    def checkout_new_branch(self, branch_name=None):
        self.repo.git.checkout(b=branch_name)
        log.info("Branch created and checked out", branch_checked_out_from=self.branch, branch_checked_out=branch_name)

    def commit_changes(self, commit_message):
        self.repo.git.add("--all")
        self.repo.index.commit(commit_message)
        log.info("Changes committed", commit_message=commit_message)

    def push_changes(self):
        origin = self.repo.remote(name='origin')
        origin.push(refspec=f'{self.new_branch_name}:{self.new_branch_name}')
        log.info("Changes pushed", pushed_to_branch=self.new_branch_name)

    def create_and_push_to_new_branch(self, commit_message):
        try:
            self.checkout_new_branch(self.new_branch_name)
            self.commit_changes(commit_message)
            self.push_changes()

        except GitCommandError as e:
            log.warning("Error creating or pushing changes to the new file", error={e})
