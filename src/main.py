from config_validator import ConfigValidator
from app_config import AppConfig
import git_service
import s3_service

secrets = AppConfig()
branch_name = "jenkins_final_test"
git = git_service.GitService(pat=secrets.git_access_key)
s3 = s3_service.S3Transfer(aws_access_key_id=secrets.aws_access_key_id,
                           aws_secret_access_key=secrets.aws_secret_access_key,
                           region_name="us-east-2")

git.repo = git.clone_repo(repo_url=f"https://x-token-auth:{secrets.bitbucket_access_token}@bitbucket.org"
                                   f"/config-generator/test.git",
                          branch="main",
                          destination="../repos/", secret=secrets.bitbucket_access_token)

# Validate yml file and convert to JSON
validator = ConfigValidator(repo_path=git.repo.working_dir,
                            json_output_path=git.repo.working_dir + "/output/test.json",
                            destination=git.repo.working_dir + "/output/",
                            schema_path="../config/cerberus_schema.yml",
                            file_name="test.yml")

git.list_remote_branches()

git.create_and_push_to_new_branch(new_branch_name=branch_name,
                                  commit_message="this has been a long effin road",
                                  bitbucket_access_key=secrets.bitbucket_access_token)

s3.upload_folder(local_folder_path=git.repo.working_dir + "/output/",
                 bucket_name="timpabucket", s3_prefix="jenkins_final_test/")
git.switch_branch("main")
git.delete_local_branch(branch_name)

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
