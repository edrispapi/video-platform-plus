import boto3
import requests

def upload_to_arvan(file_path):
    """آپلود به ArvanCloud"""
    pass  # نیاز به API Arvan

def upload_to_s3(file_path, bucket):
    """آپلود به AWS S3"""
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, file_path.split("/")[-1])
