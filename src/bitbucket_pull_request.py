from atlassian import Bitbucket

class BitbucketPullRequest:
    def __init__(self, username, password, base_url="https://bitbucket.org/"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.bitbucket = Bitbucket(
            url=self.base_url,
            username=self.username,
            password=self.password,
            timeout=60,
        )

    def create_pull_request(
        self,
        project_key,
        repository_slug,
        data,
    ):
        try:
            url = self._url_pull_requests(project_key, repository_slug)
            response = self.bitbucket.post(url, data=data)
            pull_request_url = response.get("links", {}).get("self", [{}])[0].get("href")
            print(f"Pull request created successfully. URL: {pull_request_url}")
        except Exception as e:
            print(f"Error creating pull request: {e}")

    def _url_pull_requests(self, project_key, repository_slug):
        return f"/rest/api/1.0/projects/{project_key}/repos/{repository_slug}/pull-requests"
