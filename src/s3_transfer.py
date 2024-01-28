import os

import boto3
import structlog
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

log = structlog.get_logger()


class S3Transfer:
    def __init__(self, bucket_name, local_folder_path, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        local_folder_path = local_folder_path
        self.s3_client = self._create_s3_client()

        self._upload_folder(local_folder_path, s3_prefix="test")

    def _create_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def _object_exists(self, s3_object_key):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_object_key)
            return True  # Object exists
        except self.s3_client.exceptions.NoSuchKey:
            return False  # Object does not exist
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False  # Object does not exist
            log.warning("Error checking S3 object existence", error={e})
            return None  # Unable to determine existence due to an error
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            log.warning("Error checking S3 object existence", error={e})
            return None  # Unable to determine existence due to an error

    def _upload_file(self, local_file_path, s3_object_key):
        try:
            if self._object_exists(s3_object_key):
                log.info("File already exists", file={s3_object_key}, status="Updating...")
            with open(local_file_path, 'rb') as local_file:
                self.s3_client.upload_fileobj(local_file, self.bucket_name, s3_object_key)
            log.info("File uploaded to S3 bucket", bucket_name={self.bucket_name}, uploaded_file={s3_object_key})
        except (NoCredentialsError, PartialCredentialsError):
            log.warning("AWS credentials not available. Make sure you have configured your credentials.")

    def _upload_folder(self, local_folder_path, s3_prefix=''):
        try:
            for root, dirs, files in os.walk(local_folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    s3_object_key = os.path.join(s3_prefix, relative_path).replace('\\', '/')

                    if self._object_exists(s3_object_key):
                        log.info("File already exists", file={s3_object_key}, status="Updating...")

                    with open(local_file_path, 'rb') as local_file:
                        self.s3_client.upload_fileobj(local_file, self.bucket_name, s3_object_key)

                    log.info("File uploaded to S3 bucket", bucket_name={self.bucket_name},
                             uploaded_file={s3_object_key})

            log.info("Upload complete")
        except (NoCredentialsError, PartialCredentialsError):
            log.warning("AWS credentials not available. Make sure you have configured your credentials.")
