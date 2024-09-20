# custom_storages.py
import os
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("STATIC_BUCKET_NAME")
    location = "static"


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("STATIC_BUCKET_NAME")
    location = "media"
    file_overwrite = True