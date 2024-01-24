import os
from git import Repo
from git.exc import GitCommandError


class GitService:
    def __init__(self, repo_url, branch, destination):
        self.repo_url = repo_url
        self.branch = branch
        self.repo_name = None
        self.destination = destination

    def clone_repository(self):
        # Extract the repository name from the URL
        repo_name = self.repo_url.split('/')[-1].split('.')[0]

        # Set the destination folder to the custom path with the repository name appended
        self.destination = os.path.join(self.destination, repo_name)

        try:
            # Clone the repository to the specified destination
            Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
            print(f"Repository cloned successfully to {self.destination}")
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")

    def create_pull_request(self, title, description):
        try:
            # Open the cloned repository
            repo = Repo(self.destination)

            # Create a new branch for changes
            branch_name = f"feature/{title.replace(' ', '_')}"
            repo.create_head(branch_name).checkout()

            # Commit changes (you would replace this with your actual logic)
            # For demonstration purposes, we'll just create an empty file
            with open(os.path.join(self.destination, 'example.txt'), 'w') as f:
                f.write('This is a placeholder file.')

            repo.index.add(['example.txt'])
            repo.index.commit(f"Add feature: {title}")

            # Push the changes to the new branch
            repo.git.push('--set-upstream', 'origin', branch_name)

            # Create a pull request
            pull_request = repo.create_pull(
                title=title,
                body=description,
                base='main',  # Replace with your target branch
                head=branch_name
            )

            print(f"Pull request created successfully: {pull_request.html_url}")

        except GitCommandError as e:
            print(f"Error creating pull request: {e}")

    def push_changes(self):
        try:
            # Open the cloned repository
            repo = Repo(self.destination)

            # Push changes to the remote repository
            repo.remotes.origin.push()

            print("Changes pushed successfully.")

        except GitCommandError as e:
            print(f"Error pushing changes: {e}")

# Example usage:
# git_service = GitService(repo_url='https://bitbucket.org/your_username/your_repository.git',
#                          branch='main',
#                          destination='path/to/clone')
# git_service.clone_repository()
# git_service.create_pull_request(title='Example Feature', description='This is an example feature.')
# git_service.push_changes()
