import os
import logging
import mimetypes
import boto3
from botocore.exceptions import ClientError


class AWSHandler:
    def __init__(self):
        self.s3_client = boto3.client('s3', aws_access_key_id=os.getenv('ACCESS_ID'),
                                      aws_secret_access_key=os.getenv('ACCESS_KEY'))

    # Function obtained from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    def upload_file(self, file_name, bucket, object_name):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    # Function created based on upload_file
    def delete_file(self, file_name, bucket):
        """Delete a file from an S3 bucket

        :param file_name: File to delete
        :param bucket: Bucket to delete from
        :return: Nothing
        """
        try:
            response = self.s3_client.delete_file(file_name, bucket)
        except ClientError as e:
            logging.error(e)
        return
