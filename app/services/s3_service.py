# services/s3_service.py

import boto3
from botocore.exceptions import NoCredentialsError
from core.config import settings
from botocore.config import Config

from fastapi import UploadFile

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
    config=Config(signature_version='s3v4')
)

def upload_file_to_s3(file: UploadFile, filename: str) -> str:
    try:
        s3_client.upload_fileobj(
            file.file,
            settings.aws_bucket_name,
            filename,
            ExtraArgs={
                "ContentType": file.content_type,
                # "ServerSideEncryption": "aws:kms",
                # "SSEKMSKeyId": "arn:aws:kms:ap-southeast-2:730335501238:key/9b8265d9-c9c7-4713-b0f5-9dc7db69c1cf",
                "ACL": "public-read",
                "ServerSideEncryption": "AES256"
            }
        )
        file_url = f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
        return file_url
    except NoCredentialsError:
        raise Exception("Credentials not available")
