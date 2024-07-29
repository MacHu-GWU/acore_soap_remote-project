# -*- coding: utf-8 -*-

"""
todo: docstring
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3.client import S3Client


def get_object(s3_client: "S3Client", s3uri: str) -> str:
    """
    Read an object from S3 and return its text content.
    """
    parts = s3uri.split("/", 3)
    bucket, key = parts[2], parts[3]
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")


def put_object(s3_client: "S3Client", s3uri: str, body: str):
    """
    Store a JSON object to S3.
    """
    parts = s3uri.split("/", 3)
    bucket, key = parts[2], parts[3]
    return s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
    )