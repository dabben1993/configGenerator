from atlassian.bitbucket import Bitbucket
from atlassian.bitbucket import HTTPError


class BitbucketPullRequestHandler:
    def __init__(self, username, app_password):
        self.bb = Bitbucket(url='https://api.bitbucket.org', username=username, password=app_password)

    def open_pull_request(self, project_key, repository_slug, source_branch, destination_branch, title, description):
        """
        Create a pull request on Bitbucket.

        :param project_key: Bitbucket project key.
        :param repository_slug: Bitbucket repository slug.
        :param source_branch: Source branch for the pull request.
        :param destination_branch: Destination branch for the pull request.
        :param title: Title of the pull request.
        :param description: Description of the pull request.
        :return: Response of the API call.
        """
        try:
            response = self.bb.open_pull_request(source_project=project_key, source_repo=repository_slug,
                                                 dest_project=project_key, dest_repo=repository_slug,
                                                 source_branch=source_branch, destination_branch=destination_branch,
                                                 title=title, description=description)
            return response
        except HTTPError as e:
            print(f"Error creating pull request: {e.response.content}")
            raise

    def create_pull_request(self, project_key, repository_slug, pull_request_id):
        """
        Open an existing pull request on Bitbucket.

        :param project_key: Bitbucket project key.
        :param repository_slug: Bitbucket repository slug.
        :param pull_request_id: ID of the pull request to open.
        :return: Response of the API call.
        """
        try:
            response = self.bb.create_pull_request(project_key, repository_slug, pull_request_id)
            return response
        except HTTPError as e:
            print(f"Error opening pull request: {e.response.content}")
            raise
