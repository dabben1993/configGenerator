import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


class S3Transfer:
    def __init__(self, bucket_name, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.s3_client = self._create_s3_client()

    def _create_s3_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def object_exists(self, s3_object_key):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_object_key)
            return True  # Object exists
        except self.s3_client.exceptions.NoSuchKey:
            return False  # Object does not exist
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            print(f"Error checking S3 object existence: {e}")
            return None  # Unable to determine existence due to an error

    def upload_file(self, local_file_path, s3_object_key):
        try:
            if self.object_exists(s3_object_key):
                print(f"File '{s3_object_key}' already exists in S3 bucket. Updating...")
            with open(local_file_path, 'rb') as local_file:
                self.s3_client.upload_fileobj(local_file, self.bucket_name, s3_object_key)
            print(f"File uploaded to S3 bucket: {self.bucket_name}/{s3_object_key}")
        except (NoCredentialsError, PartialCredentialsError):
            print("AWS credentials not available. Make sure you have configured your credentials.")

# Example usage:
# s3_transfer = S3Transfer(bucket_name='your-s3-bucket', aws_access_key_id='your-access-key', aws_secret_access_key='your-secret-key', region_name='your-region')
# s3_transfer.upload_file(local_file_path='output/test.json', s3_object_key='output/test.json')
