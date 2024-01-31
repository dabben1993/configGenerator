import logging

from config_validator import ConfigValidator
from src.app_config import AppConfig
import git_service
import s3_service

secrets = AppConfig()
git = git_service.GitService(pat=secrets.git_access_key)
s3 = s3_service.S3Transfer(aws_access_key_id=secrets.aws_access_key_id,
                           aws_secret_access_key=secrets.aws_secret_access_key,
                           region_name="us-east-2")

git.repo = git.clone_repo(repo_url="https://dabben93@bitbucket.org/config-generator/test.git",
                          branch="main",
                          destination="../repos/")

# Validate yml file and convert to JSON
validator = ConfigValidator(repo_path=git.repo.working_dir,
                            json_output_path=git.repo.working_dir + "/output/test.json",
                            destination="../repos/test/output/",
                            schema_path="../config/cerberus_schema.yml",
                            file_name="test.yml")

git.list_remote_branches()

# Upload it to s3 Bucket
git.create_and_push_to_new_branch(new_branch_name="final_refactortr",
                                  commit_message="this is commit 215332")
s3.list_all_objects("timpabucket")

s3.upload_folder(local_folder_path="../repos/test/output/",
                         bucket_name="timpabucket", s3_prefix="final/")
s3.download_folder("timpabucket", "final/", "../tests/final")
git.switch_branch("main")


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
