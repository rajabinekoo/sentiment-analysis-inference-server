import os
import boto3


class S3Storage:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("S3_URL"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            region_name=os.getenv("S3_REGION"),
        )

    def download_directory(self, bucket_name: str, minio_prefix: str, local_directory_path: str):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=minio_prefix)
            if 'Contents' in response:
                for obj in response['Contents']:
                    object_key = obj['Key']
                    relative_path = object_key[len(minio_prefix):]
                    local_file_path = os.path.join(local_directory_path, relative_path)
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                    if object_key.endswith('/'):
                        continue
                    try:
                        self.s3_client.download_file(bucket_name, object_key, local_file_path)
                    except Exception as e:
                        print(f"Directory downloading failed: ('{object_key}': {e})")
        except Exception as e:
            print(f"Directory downloading failed: {e}")
