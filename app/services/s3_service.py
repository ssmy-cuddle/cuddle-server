# services/s3_service.py

import boto3
from botocore.exceptions import NoCredentialsError
from core.config import settings
from fastapi import UploadFile

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

def upload_file_to_s3(file: UploadFile, filename: str) -> str:
    try:
        s3_client.upload_fileobj(
            file.file,
            settings.aws_bucket_name,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        file_url = f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
        return file_url
    except NoCredentialsError:
        raise Exception("Credentials not available")
