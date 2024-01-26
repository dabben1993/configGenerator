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

    def _clone_repo(self):

        # Extract the repository name from the URL
        repo_name = self.repo_url.split('/')[-1].split('.')[0]

        # Set the destination folder to the custom path with the repository name appended
        self.destination = os.path.join(self.destination, repo_name)

        # Check if the repository already exists in the specified destination
        if os.path.exists(self.destination):
            repo = Repo(self.destination)
            log.info("Repository exists", repository=repo_name, status="Updating...")
            # Pull latest changes from the remote repository
            origin = repo.remote(name='origin')
            origin.pull()
        else:
            # Clone the repository if it doesn't exist
            repo = Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
            log.info("Repository cloned successfully", repository=repo_name, status="Cloned successfully")
        return repo

    def create_and_push_to_new_branch(self, commit_message):
        try:
            # Create and switch to a new branch
            self.repo.git.checkout(b=self.new_branch_name)
            print(f"New branch '{self.new_branch_name}' created and checked out.")
            log.info("New branch created and checked out", checked_out_from_branch=self.branch,
                     branch_created=self.new_branch_name)

            # Add all changes
            self.repo.git.add("--all")

            # Commit changes
            self.repo.index.commit(commit_message)
            log.info("Changes committed", commit_message=commit_message)

            # Push the new branch to the remote repository
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.new_branch_name}:{self.new_branch_name}')
            log.info("Changes pushed", pushed_to_branch=self.new_branch_name)

        except GitCommandError as e:
            log.warning("Error creating or pushing changes to the new file", error={e})
