from config_validator import ConfigValidator
from src.app_config import AppConfig
import git_service
import s3_service
from src.service_exception import ServiceException

secrets = AppConfig()
git = git_service.GitService(pat=secrets.git_access_key)
s3 = s3_service.S3Transfer(aws_access_key_id=secrets.aws_access_key_id,
                           aws_secret_access_key=secrets.aws_secret_access_key,
                           region_name="us-east-2")

# git.repo = git.clone_repo(repo_url="https://dabben93@bitbucket.org/config-generator/test.git",
#                          branch="main",
#                          destination="../repos/")
# git.create_and_push_to_new_branch(new_branch_name="test_refactor",
#                                  commit_message="This is commit #5123")
# Validate yml file and convert to JSON
# validator = ConfigValidator(file_path="../repos/test/yml/test.yml",
#                            json_output_path="../repos/test/output/test.json",
#                            destination="../repos/test/output/",
#                            schema_path="../config/cerberus_schema.yml")

# git_service.list_remote_branches(repository)
# Upload it to s3 Bucket
# service = s3_service.create_s3_client(s3)
try:
    s3.download_file("timpabucket", "testy.json", "../tests/test.json")
    s3.list_all_objects("timpabucketsf")

except ServiceException as se:
    raise ServiceException("Errors occured", original_exception=se)
# s3.list_objects_in_folder("timpabucket", "test/")
# s3_service.upload_folder(s3_client=service, local_folder_path="../repos/test/output/",
#                         bucket_name="timpabucket")
# s3_service.download_file(service, "timpabucket", "test.json", "../tests/test.json")
# s3_service.download_folder(service, "timpabucket", "output/", "../tests/tests")
# git_service.create_and_push_to_new_branch(repository=repository, new_branch_name="freshly_pressed",
#                                          commit_message="This is commit #5123")
# git_service.switch_branch(repository, "main")
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
