import set_env_vars

import os

from src.git_service import GitService
from config_validator import ConfigValidator

# Run the function from set_env_vars to set AWS credentials
set_env_vars.set_aws_credentials()


# Retrieve environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

print("access key: " + aws_access_key_id)
print("secret key: " + aws_secret_access_key)

# Try to import repo

git_service = GitService(
    repo_url="https://dabben93@bitbucket.org/config-generator/test.git",
    branch="main",
    destination="../repos/"
)

git_service.clone_repository()

validator = ConfigValidator()
print(git_service.destination)
validator.validate_yml(file_path=git_service.destination + "/yml/test.yml")
