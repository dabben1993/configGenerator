import os
from git import Repo, repo
from git.exc import GitCommandError
import structlog

from src.service_exception import ServiceException


class GitService:
    def __init__(self, pat=None, user_name=None, password=None):
        self.pat = pat
        self.user_name = user_name
        self.password = password
        self.repo = Repo
        self.log = structlog.get_logger()

    def _get_repo_name(self, repo_url):
        try:
            repo_name = repo_url.split('/')[-1].split('.')[0]
            self.log.info("Repo name extraced", repo_name=repo_name)
            return repo_name
        except Exception as e:
            self.log.warning("Error extracting repo name", error=str(e))
            raise

    def clone_new_repo(self, repo_url, destination, branch):
        try:
            repo = Repo.clone_from(repo_url, destination, branch=branch)
            self.log.info("Repository cloned successfully", repo=self._get_repo_name(repo_url),
                          url=repo_url, branch=branch, status="Cloned successfully")
            return repo
        except Exception as e:
            self.log.warning("Error cloning new repository", error=str(e))
            raise

    def update_existing_repo(self, repo_name, destination):
        try:
            self.log.info("Repository exists", repo=repo_name, status="Updating...")
            repo = Repo(destination)
            repo.remotes.origin.pull()
            self.log.info("Repository updated", repo=repo_name, destination=destination,
                          status="Updated")
            return repo
        except TypeError as git_error:
            self.log.error("Error updating existing repository", error=str(git_error))
            raise ServiceException("Error updating existing repository",
                                   original_exception=str(git_error))

    def clone_repo(self, repo_url, destination, branch):
        try:
            repo_name = self._get_repo_name(repo_url)
            destination = os.path.join(destination, repo_name)

            if os.path.exists(destination):
                return self.update_existing_repo(repo_name=repo_name, destination=destination)
            else:
                return self.clone_new_repo(repo_url=repo_url, destination=destination, branch=branch)
        except Exception as e:
            self.log.warning("Error cloning repository", error=str(e))
            raise ServiceException("Error cloning repository",
                                   original_exception=e)

    def list_remote_branches(self):
        try:
            self.log.info("Fetching remote branches")
            remote_branches = [ref.name.split('/')[-1] for ref in self.repo.remotes.origin.refs if ref.remote_head]

            self.log.info("Remote branches:")
            for branch in remote_branches:
                self.log.info("Branch", branch_name=branch)

        except Exception as e:
            self.log.warning("Error listing remote branches", error=str(e))
            raise

    def checkout_new_branch(self, branch_name):
        try:
            checked_out_branch = self.repo.active_branch.name
            self.repo.git.checkout(b=branch_name)
            self.log.info("Branch created and checked out", branch_checked_out_from=checked_out_branch,
                          branch_checked_out=branch_name)
        except Exception as e:
            self.log.warning("Error checking out new branch", error=str(e))
            raise ServiceException("Error checking out new branch",
                                   original_exception=e)

    def switch_branch(self, branch_name):
        try:
            checked_out_branch = self.repo.active_branch.name
            self.repo.git.switch(branch_name)
            self.log.info("Switched branch", branch_checked_out_from=checked_out_branch,
                          branch_checked_out=branch_name)
        except Exception as e:
            self.log.warning("Error switching new branch", error=str(e))
            raise ServiceException("Error switching branches",
                                   original_exception=e)

    def commit_changes(self, commit_message):
        try:
            self.repo.git.add("--all")
            self.repo.index.commit(commit_message)
            self.log.info("Changes committed", commit_message=commit_message)
        except Exception as e:
            self.log.warning("Error committing changes", error=str(e))
            raise ServiceException("Error committing changes",
                                   original_exception=e)

    def push_changes(self):
        try:
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.repo.active_branch.name}:{self.repo.active_branch.name}')
            self.log.info("Changes pushed", pushed_to_branch=self.repo.active_branch.name)
        except GitCommandError as e:
            self.log.warning("Error pushing changes to the remote repository", error=str(e))
            raise ServiceException("Error pushing changes to remote repository",
                                   original_exception=e)

    def create_and_push_to_new_branch(self, new_branch_name, commit_message):
        try:
            self.checkout_new_branch(branch_name=new_branch_name)
            self.commit_changes(commit_message=commit_message)
            self.push_changes()
            self.switch_branch('main')

        except ServiceException as e:
            self.log.warning("Error creating or pushing changes to the new file", error={e})
            raise ServiceException("Errors occured", original_exception=e)
