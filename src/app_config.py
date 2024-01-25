import configparser
import os


class AppConfig:
    def __init__(self):
        self._bitbucket_username = None
        self._bitbucket_app_password = None
        self._aws_access_key_id = None
        self._aws_secret_access_key = None

    @property
    def bitbucket_username(self):
        if not self._bitbucket_username:
            self._bitbucket_username = os.getenv("BITBUCKET_USERNAME")
        return self._bitbucket_username

    @property
    def bitbucket_app_password(self):
        if not self._bitbucket_app_password:
            self._bitbucket_app_password = os.getenv("BITBUCKET_APP_PASS")
        return self._bitbucket_app_password

    @property
    def aws_access_key_id(self):
        if not self._aws_access_key_id:
            self._aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        return self._aws_access_key_id

    @property
    def aws_secret_access_key(self):
        if not self._aws_secret_access_key:
            self._aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        return self._aws_secret_access_key
