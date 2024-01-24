import os
import configparser

def set_aws_credentials():
    config = configparser.ConfigParser()
    config.read('config/config.ini')  # Adjust the path if the config file is in a different location

    # Set your AWS credentials
    os.environ["AWS_ACCESS_KEY_ID"] = config.get('aws_credentials', 'AWS_ACCESS_KEY_ID')
    os.environ["AWS_SECRET_ACCESS_KEY"] = config.get('aws_credentials', 'AWS_SECRET_ACCESS_KEY')

if __name__ == "__main__":
    set_aws_credentials()
