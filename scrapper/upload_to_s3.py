import boto3
from botocore.client import Config
import os
ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'kushal-jewels'

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id='AKIAQNL5LVB3ZWB3MQC3',
    aws_secret_access_key='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',
)

#upload images to the s3 bucket
root_folder = '../images'
for folder_name in [x for x in os.listdir(root_folder) if x!= '.DS_Store']:
    sub_folder = root_folder+'/'+folder_name+'/'
    for file_name in [x for x in os.listdir(sub_folder) if x!='.DS_Store']:
        s3.Bucket(BUCKET_NAME).put_object(Key=sub_folder[3:]+file_name, Body=open(sub_folder+file_name, 'rb'), ACL='public-read')

print ("all the images are uploaded !!")
