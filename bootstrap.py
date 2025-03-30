import os
from dotenv import load_dotenv

from libs.s3_storage import S3Storage
from libs.spark import spark_app

load_dotenv()

s3_storage = S3Storage()
spark_app.init()


def bootstrap():
    local_path = os.getenv("S3_LOCAL_MODEL_DIR")
    if not local_path:
        raise ValueError("S3_LOCAL_MODEL_DIR environment variable not defined")
    if os.path.isdir(local_path):
        return

    bucket = os.getenv("S3_BUCKET_MODEL")
    remote_path = os.getenv("S3_REMOTE_MODEL_DIR")
    if not bucket:
        raise ValueError("S3_BUCKET_MODEL environment variable not defined")
    if not remote_path:
        raise ValueError("S3_REMOTE_MODEL_DIR environment variable not defined")
    s3_storage.download_directory(bucket, remote_path, local_path)
