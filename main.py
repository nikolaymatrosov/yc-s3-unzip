import os
import re
import zipfile
from io import BytesIO

import boto3 as boto3
import pydash as pydash

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


def handler(event: dict, context):
    session = boto3.session.Session()

    client = session.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    bucket_id = pydash.get(event, 'messages[0].details.bucket_id')
    object_id = pydash.get(event, 'messages[0].details.object_id')
    if not re.search(r'\.zip$', object_id):
        print('Doesnt match')
        return
    zip_obj = client.get_object(Bucket=bucket_id, Key=object_id)

    buffer = BytesIO(zip_obj["Body"].read())

    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        print(file_info)
        client.upload_fileobj(
            z.open(filename),
            Bucket=bucket_id,
            Key=f'{filename}'
        )
