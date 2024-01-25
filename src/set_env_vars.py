import os
import configparser


def set_aws_credentials():
    config = configparser.ConfigParser()
    config.read('../config/config.ini')

    # Set env vars
    os.environ["AWS_ACCESS_KEY_ID"] = config.get('aws_credentials', 'AWS_ACCESS_KEY_ID')
    os.environ["AWS_SECRET_ACCESS_KEY"] = config.get('aws_credentials', 'AWS_SECRET_ACCESS_KEY')
    os.environ["BITBUCKET_APP_PASS"] = config.get('bitbucket', 'BITBUCKET_APP_PASS')
    os.environ["BITBUCKET_USERNAME"] = config.get('bitbucket', 'BITBUCKET_USERNAME')


if __name__ == "__main__":
    set_aws_credentials()
