import os
from git import Repo
from git.exc import GitCommandError


class GitService:
    def __init__(self, repo_url, branch, destination):
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
            print("Repository already exists. Updating...")
            # Pull latest changes from the remote repository
            origin = repo.remote(name='origin')
            origin.pull()
        else:
            # Clone the repository if it doesn't exist
            repo = Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
            print("Repository cloned successfully.")
        return repo

    def commit_and_push(self, commit_message):
        try:
            # Add all changes
            self.repo.git.add("--all")

            # Commit changes
            self.repo.index.commit(commit_message)

            # Push to the remote repository
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.branch}:{self.branch}')
            print("Changes committed and pushed successfully.")
        except GitCommandError as e:
            print(f"Error committing and pushing changes: {e}")

    def create_pull_request(self, title, description):
        try:
            # Create a pull request
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.branch}:{self.branch}')
            pull_request_url = f'{self.repo_url}/pull-requests/new?source={self.branch}&title={title}&description={description}'
            print(f"Pull request created. Open the following link to review and merge:\n{pull_request_url}")
        except GitCommandError as e:
            print(f"Error creating pull request: {e}")


# Example usage:
# git_service = GitService(repo_url='https://bitbucket.org/your_username/your_repository.git',
#                          branch='main',
#                          destination='path/to/clone')
# git_service.clone_repository()
# git_service.create_pull_request(title='Example Feature', description='This is an example feature.')
# git_service.push_changes()
