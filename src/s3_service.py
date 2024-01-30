import os

import boto3
import botocore
import structlog
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

log = structlog.get_logger()


def object_exists(s3_client, bucket_name, s3_object_key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_object_key)
        return True  # Object exists
    except s3_client.exceptions.NoSuchKey:
        return False  # Object does not exist
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False  # Object does not exist
        log.warning("Error checking S3 object existence", error={e})
        return None  # Unable to determine existence due to an error
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        log.warning("Error checking S3 object existence", error={e})
        return None  # Unable to determine existence due to an error


def upload_file(s3_client, local_file_path, s3_object_key, bucket_name):
    try:
        if object_exists(s3_client=s3_client, bucket_name=bucket_name, s3_object_key=s3_object_key):
            log.info("File already exists", file={s3_object_key}, status="Updating...")
        with open(local_file_path, 'rb') as local_file:
            s3_client.upload_fileobj(local_file, bucket_name, s3_object_key)
        log.info("File uploaded to S3 bucket", bucket_name={bucket_name}, uploaded_file={s3_object_key})
    except (NoCredentialsError, PartialCredentialsError):
        log.warning("AWS credentials not available. Make sure you have configured your credentials.")


def upload_folder(s3_client, local_folder_path, bucket_name, s3_prefix=''):
    try:
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_folder_path)
                s3_object_key = os.path.join(s3_prefix, relative_path).replace('\\', '/')

                if object_exists(s3_client=s3_client, bucket_name=bucket_name, s3_object_key=s3_object_key):
                    log.info("File already exists", file={s3_object_key}, status="Updating...")

                with open(local_file_path, 'rb') as local_file:
                    s3_client.upload_fileobj(local_file, bucket_name, s3_object_key)

                log.info("File uploaded to S3 bucket", bucket_name={bucket_name},
                         uploaded_file={s3_object_key})

        log.info("Upload complete")
    except (NoCredentialsError, PartialCredentialsError):
        log.warning("AWS credentials not available. Make sure you have configured your credentials.")


def download_file(s3_client, bucket_name, object_key, destination):
    try:
        log.info("Downloading file from S3", bucket=bucket_name, object_key=object_key)
        s3_client.download_file(Bucket=bucket_name, Key=object_key, Filename=destination)
        log.info("File downloaded successfully", destination=destination)
    except botocore.exceptions.ClientError as e:
        log.error("Error downloading file from S3", error=str(e))
        raise


def download_folder(s3_client, bucket_name, prefix, destination):
    try:
        log.info("Downloading folder from S3", bucket=bucket_name, prefix=prefix)
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if not os.path.exists(destination):
            os.makedirs(destination)

        for obj in objects.get("Contents", []):
            key = obj["Key"]
            dest_file_path = os.path.join(destination, os.path.relpath(key, prefix))
            download_file(s3_client=s3_client, bucket_name=bucket_name,
                          object_key=key, destination=dest_file_path)

        log.info("Folder downloaded successfully", destination_path=destination)
    except botocore.exceptions.ClientError as e:
        log.error("Error downloading folder from S3", error=str(e))
        raise


def create_s3_client(secrets):
    return boto3.client(
        's3',
        aws_access_key_id=secrets.aws_access_key_id,
        aws_secret_access_key=secrets.aws_secret_access_key,
        region_name=secrets.region_name
    )


class S3Transfer:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name