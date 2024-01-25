import base64
import os
from base64 import b64encode

import requests

from git import Repo
from git.exc import GitCommandError


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
            print("Repository already exists. Updating...")
            # Pull latest changes from the remote repository
            origin = repo.remote(name='origin')
            origin.pull()
        else:
            # Clone the repository if it doesn't exist
            repo = Repo.clone_from(self.repo_url, self.destination, branch=self.branch)
            print("Repository cloned successfully.")
        return repo

    def create_and_push_to_new_branch(self, commit_message):
        try:
            # Create and switch to a new branch
            self.repo.git.checkout(b=self.new_branch_name)
            print(f"New branch '{self.new_branch_name}' created and checked out.")

            # Add all changes
            self.repo.git.add("--all")

            # Commit changes
            self.repo.index.commit(commit_message)
            print(f"Changes committed with message: '{commit_message}'.")

            # Push the new branch to the remote repository
            origin = self.repo.remote(name='origin')
            origin.push(refspec=f'{self.new_branch_name}:{self.new_branch_name}')
            print(f"Changes pushed to the remote branch '{self.new_branch_name}'.")

        except GitCommandError as e:
            print(f"Error creating or pushing changes to the new branch: {e}")

    def create_pull_request(self, source_branch, destination_branch, title, description):

        # Bitbucket REST API endpoint for creating a pull request
        api_url = "https://api.bitbucket.org/2.0/repositories/config-generator/test/pullrequests"

        print(api_url)

        # Prepare the payload for the API request
        payload = {
            "title": title,
            "description": description,
            "source": {
                "branch": {"name": source_branch}
            },
            "destination": {
                "branch": {"name": destination_branch}
            }
        }

        # Set authentication headers using the app password
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{os.getenv("BITBUCKET_USERNAME")}:{os.getenv("BITBUCKET_APP_PASSWORD")}'.encode()).decode()}",
        }

        print("Authentication Header:", headers)
        print("Payload:", payload)

        # Make the API request
        response = requests.request("POST", api_url, data=payload, headers=headers)

        # Check the response status
        if response.status_code == 201:
            print("Pull request created successfully.")
        else:
            print(f"Failed to create pull request. Status code: {response.status_code}, Error: {response.text}")
