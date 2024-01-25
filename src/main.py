import set_env_vars

import os

from src.app_config import AppConfig
from src.git_service import GitService
from config_validator import ConfigValidator
from s3_transfer import S3Transfer
from bitbucket_pull_request import BitbucketPullRequestHandler

set_env_vars.set_aws_credentials()

secrets = AppConfig()

# Import repo
git_service = GitService(
    repo_url="https://dabben93@bitbucket.org/config-generator/test.git",
    branch="main",
    destination="../repos/",
    new_branch_name="newTest"
)

# Validate yml file and convert to JSON
validator = ConfigValidator(file_path=git_service.destination + "/yml/test.yml",
                            json_output_path=git_service.destination + "/output/test.json",
                            destination=git_service.destination + "/output/",
                            schema_path="../config/cerberus_schema.yml")
# print(git_service.destination)
# validator.validate_yml(file_path=git_service.destination + "/yml/test.yml")
# validator.convert_to_json(file_path=git_service.destination + "/yml/test.yml",
#                          json_output_path=git_service.destination + "/output/test.json")

# Upload it to s3 Bucket
s3_transfer = S3Transfer(bucket_name='timpabucket', aws_access_key_id=secrets.aws_access_key_id,
                         aws_secret_access_key=secrets.aws_secret_access_key, region_name="us-east-2",
                         local_folder_path=git_service.destination + "/output/")
# s3_transfer.upload_file(local_file_path=git_service.destination + "/output/test.json", s3_object_key="output/test.json")

# Commit, push and pull request
git_service.create_and_push_to_new_branch(commit_message="This is a commit")
bitbucket_pull_request = BitbucketPullRequestHandler(username=secrets.bitbucket_username,
                                                     app_password=secrets.bitbucket_app_password)

bitbucket_pull_request.open_pull_request(project_key="config-generator",
                                                    repository_slug="test",
                                                    source_branch="newTest",
                                                    destination_branch="main",
                                                    title="Generic Title",
                                                    description="Lorem ipsum")

# git_service.create_pull_request(source_branch=git_service.new_branch_name,
#                                destination_branch=git_service.branch,
#                                title="Generic title",
#                                description="Lorem ipsum")
