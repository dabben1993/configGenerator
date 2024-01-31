import os

import boto3
import botocore
import structlog
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from service_exception import ServiceException

log = structlog.get_logger()


class S3Transfer:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.s3_client = self._create_s3_client()

    def object_exists(self, bucket_name, s3_object_key):
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=s3_object_key)
            return True  # Object exists
        except self.s3_client.exceptions.NoSuchKey:
            return False  # Object does not exist
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False  # Object does not exist
            log.warning("Object does not exist", error={e})
            return ServiceException("Object does not exist", original_exception=e)
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            log.warning("AWS credentials not available", error={e})
            return ServiceException("AWS credentials not available", original_exception=e)

    def upload_file(self, local_file_path, s3_object_key, bucket_name):
        try:
            if self.object_exists(bucket_name=bucket_name, s3_object_key=s3_object_key):
                log.info("File already exists", file={s3_object_key}, status="Updating...")
            with open(local_file_path, 'rb') as local_file:
                self.s3_client.upload_fileobj(local_file, bucket_name, s3_object_key)
            log.info("File uploaded to S3 bucket", bucket_name={bucket_name}, uploaded_file={s3_object_key})
        except (NoCredentialsError, PartialCredentialsError) as e:
            log.warning("AWS credentials not available. Make sure you have configured your credentials.")
            return ServiceException("AWS credentials not available", original_exception=e)

    def upload_folder(self, local_folder_path, bucket_name, s3_prefix=''):
        try:
            for root, dirs, files in os.walk(local_folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    s3_object_key = os.path.join(s3_prefix, relative_path).replace('\\', '/')

                    if self.object_exists(bucket_name=bucket_name, s3_object_key=s3_object_key):
                        log.info("File already exists", file={s3_object_key}, status="Updating...")

                    with open(local_file_path, 'rb') as local_file:
                        self.s3_client.upload_fileobj(local_file, bucket_name, s3_object_key)

                    log.info("File uploaded to S3 bucket", bucket_name={bucket_name},
                             uploaded_file={s3_object_key})

            log.info("Upload complete")
        except (NoCredentialsError, PartialCredentialsError) as e:
            log.warning("AWS credentials not available. Make sure you have configured your credentials.")
            return ServiceException("AWS credentials not available", original_exception=e)

    def download_file(self, bucket_name, object_key, destination):
        try:
            log.info("Downloading file from S3", bucket=bucket_name, object_key=object_key)
            self.s3_client.download_file(Bucket=bucket_name, Key=object_key, Filename=destination)
            log.info("File downloaded successfully", destination=destination)
        except botocore.exceptions.ClientError as e:
            log.error("Error downloading file from S3", error=str(e))
            return ServiceException("Error downloading file from S3", original_exception=e)

    def download_folder(self, bucket_name, prefix, destination):
        try:
            log.info("Downloading folder from S3", bucket=bucket_name, prefix=prefix)
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if not os.path.exists(destination):
                os.makedirs(destination)

            for obj in objects.get("Contents", []):
                key = obj["Key"]
                dest_file_path = os.path.join(destination, os.path.relpath(key, prefix))
                self.download_file(bucket_name=bucket_name,
                                   object_key=key, destination=dest_file_path)

            log.info("Folder downloaded successfully", destination_path=destination)
        except botocore.exceptions.ClientError as e:
            log.error("Error downloading folder from S3", error=str(e))
            return ServiceException("Error downloading folder from S3", original_exception=e)

    def list_all_objects(self, bucket_name):
        try:
            log.info("Listing all items in bucket", bucket_name=bucket_name)
            response = self.s3_client.list_objects(Bucket=bucket_name)
            for obj in response.get('Contents', []):
                log.info("Item", item_name=obj['Key'])
        except botocore.exceptions.ClientError as e:
            log.error("Error listing objects from S3", error=str(e))
            return ServiceException("Error listing objects from S3", original_exception=e)

    def list_objects_in_folder(self, bucket_name, prefix):
        try:
            log.info("Listing objects in folder", bucket=bucket_name, folder=prefix)
            response = self.s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)
            for obj in response.get('Contents', []):
                log.info("Item", item_name=obj['Key'])
        except botocore.exceptions.ClientError as e:
            log.error("Error listing objects from S3", error=str(e))
            return ServiceException("Error downloading folder from S3", original_exception=e)

    def _create_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
