import os

import boto3

from dotenv import load_dotenv

from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


session = boto3.Session(
    aws_access_key_id=os.getenv('ACCESS_KEY_AWS'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY_AWS'),
)

# Let's use Amazon S3
s3 = session.resource("s3")

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

