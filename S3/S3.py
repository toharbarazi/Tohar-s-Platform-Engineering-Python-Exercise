import boto3
import json
import pulumi
import pulumi_aws as aws
from pulumi import FileAsset
import boto3
from botocore.exceptions import ClientError


def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def create_S3():
    config = load_config()
    s3 = boto3.client('s3')
    bucket_name =config[0]["name"]
    if config[0]["access"] == "public":
        access_value=False
    else:
        access_value=True
    s3.create_bucket(Bucket=bucket_name)
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': access_value,
            'BlockPublicPolicy': access_value,
            'IgnorePublicAcls': access_value,
            'RestrictPublicBuckets': access_value
        }
    )
    # Add a tag to the S3 bucket
    s3.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={
            'TagSet': [
                {
                    'Key': 'Platform',
                    'Value': 'CLI'
                },
                {
                    'Key': 'Owner',
                    'Value': config[0]["owner"]
                }
            ]
        }
    )
    print(f"Bucket {bucket_name} created with public access.")

def upload_files():
    config = load_config()
    bucket_name = config[0]["S3_name"]
    file_path = config[0]["path"]
    file_name = config[0]["file_name"]

    bucket_object = aws.s3.BucketObject(
        file_name,
        bucket=bucket_name,
        source=FileAsset(file_path),  # Correct way to upload a file using FileAsset
        acl="private",  # Make the file publicly readable
    )

    print(f"File '{file_name}' uploaded to bucket '{bucket_name}'.")

def list_s3():
    config = load_config()
    s3 = boto3.client('s3')
    filtered_buckets = []
    all_buckets = s3.list_buckets()
    for bucket in all_buckets['Buckets']:
        bucket_name = bucket['Name']

        try:
            tags_response = s3.get_bucket_tagging(Bucket=bucket_name)

            for tag in tags_response.get('TagSet', []):
                if (tag['Key'] == 'Platform' and tag['Value'] == 'CLI') and (tag['Key'] == 'owner' and tag['Value'] == config[0]["owner"])  :
                    filtered_buckets.append(bucket_name)
                    break
        except ClientError as e:
            continue

    print("S3 buckets that created through the cli:", filtered_buckets)

#chatgpt says this the right version, try later
# import boto3
# from botocore.exceptions import ClientError
# def list_s3():
#     config = load_config()  # Make sure this function is defined
#     s3 = boto3.client('s3')
#     filtered_buckets = []
#
#     # Get all buckets
#     all_buckets = s3.list_buckets()
#     for bucket in all_buckets['Buckets']:
#         bucket_name = bucket['Name']
#
#         try:
#             # Get tags for the bucket
#             tags_response = s3.get_bucket_tagging(Bucket=bucket_name)
#             tags = tags_response.get('TagSet', [])
#
#             # Check for both tags: Platform = CLI and Owner = config[0]["owner"]
#             has_platform_tag = False
#             has_owner_tag = False
#
#             for tag in tags:
#                 if tag['Key'] == 'Platform' and tag['Value'] == 'CLI':
#                     has_platform_tag = True
#                 if tag['Key'] == 'Owner' and tag['Value'] == config[0]["owner"]:
#                     has_owner_tag = True
#
#             # If both tags are present, add to filtered list
#             if has_platform_tag and has_owner_tag:
#                 filtered_buckets.append(bucket_name)
#
#         except ClientError as e:
#             # Continue if the bucket has no tags or access is denied
#             continue
#
#     # Print the filtered buckets
#     print("S3 buckets created through the CLI by the specified owner:")
#     for i, bucket_name in enumerate(filtered_buckets):
#         print(f"{i + 1}. {bucket_name}")
#
#     return filtered_buckets


