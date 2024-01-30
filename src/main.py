from config_validator import ConfigValidator
from s3_transfer import S3Transfer
from src.app_config import AppConfig
import git_service

secrets = AppConfig()
# Import repo
git = git_service.GitService(
    PAT=secrets.git_access_key
)
repository = git_service.clone_repo(repo_url="https://dabben93@bitbucket.org/config-generator/test.git",
                       branch="main",
                       destination="../repos/", )

# Validate yml file and convert to JSON
validator = ConfigValidator(file_path= "../repos/test/yml/test.yml",
                            json_output_path="../repos/test/output/test.json",
                            destination="../repos/test/output/",
                            schema_path="../config/cerberus_schema.yml")

# Upload it to s3 Bucket
s3_transfer = S3Transfer(bucket_name='timpabucket', aws_access_key_id=secrets.aws_access_key_id,
                         aws_secret_access_key=secrets.aws_secret_access_key, region_name="us-east-2",
                         local_folder_path="../repos/test/output/")

# Commit, push and pull request
git_service.create_and_push_to_new_branch(repository=repository, new_branch_name="neqw_branch",
                                          commit_message="This is commit #5123")
# bitbucket_pull_request = BitbucketPullRequestHandler(username=secrets.bitbucket_username,
#                                                     app_password=secrets.bitbucket_app_password)
#
# bitbucket_pull_request.open_pull_request(project_key="test1",
#                                         repository_slug="test",
#                                         source_branch="newTest",
#                                         destination_branch="main",
#                                         title="Generic Title",
#                                         description="Lorem ipsum")

# git_service.create_pull_request(source_branch=git_service.new_branch_name,
#                                destination_branch=git_service.branch,
#                                title="Generic title",
#                                description="Lorem ipsum")
