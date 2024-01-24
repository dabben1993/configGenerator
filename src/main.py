import set_env_vars

# Run the function from set_env_vars to set AWS credentials
set_env_vars.set_aws_credentials()

import os

# Retrieve environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Rest of your main script logic...
