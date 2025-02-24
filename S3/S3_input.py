import boto3
import re
from pathlib import Path


def is_valid_s3_bucket_name(name):
    # Check length of the name
    if not (3 <= len(name) <= 63):
        print("Bucket name must be between 3 and 63 characters.")
        return False

    # Check for lowercase letters, numbers, and hyphens only
    if not re.match(r'^[a-z0-9-]+$', name):
        print("Bucket name can only contain lowercase letters, numbers, and hyphens.")
        return False

    # Check if the name starts or ends with a hyphen
    if name[0] == '-' or name[-1] == '-':
        print("Bucket name cannot start or end with a hyphen.")
        return False

    # Check if the name contains consecutive hyphens
    if '--' in name:
        print("Bucket name cannot contain consecutive hyphens.")
        return False

    # If the name passes all checks, it is valid
    print("Bucket name is valid.")
    return True


def create_S3_input():
    name = input("The name of your S3: ")
    valid_name=is_valid_s3_bucket_name(name)
    while valid_name==False:
        name = input("invalid bucket name. Please name it again: ")
        valid_name = is_valid_s3_bucket_name(name)

    owner = input("Who is the owner of the S3: ")
    access = input("Would you like to give your S3 public/private access? ")

    while access not in ["public", "private"]:  # Add more options later like PUBLIC etc
        access = input("Invalid input. Please choose public or private: ")

    if access == "public":
        confirmation = input("Are you sure you want to create PUBLIC S3? Y/N: ")
        if confirmation.lower() != "y":
            print("Bucket creation cancelled.")
            return None
        else:
            return {
                "name": name,
                "owner": owner,
                "access": access,
            },"create_S3"


    else:
        return {
        "name": name,
        "access": access,
    },"create_S3"


def check_if_path_exists(path):
    # Check if the path exists
    if Path(path).exists():
        print("The path exists locally.")
        return True  # Return True if the path exists
    else:
        print("The path does NOT exist locally.")
        return False  # Return False if the path doesn't exist

def S3_upload_files_input():
    s3 = boto3.client('s3')

    while True:
        S3_name = input("Enter the name of the S3 you would like to add files to: ")
        print(f"Checking if the bucket '{S3_name}' exists and was created through the CLI...")
        response = s3.get_bucket_tagging(Bucket=S3_name)
        tags = response.get('TagSet', [])
        platform_tag_found = False
        for tag in tags:
            if tag.get('Key') == 'Platform' and tag.get('Value') == 'CLI':
                platform_tag_found = True
                break

        if platform_tag_found:
            print("Confirmed")
            path=input(f"Enter path to the file you would like to upload to '{S3_name}: ")
            path=path.replace("'", "").replace('"', "")
            path_exist=check_if_path_exists(path)
            while path_exist==False:
                path_exist=input("The path does NOT exist locally. Please enter new path: ")
                path = path.replace("'", "").replace('"', "")
                path_exist = check_if_path_exists(path)

            file_name=input("Name the file inside the S3: ")
            return {
                "S3_name": S3_name,
                "path": path,
                "file_name": file_name,

            },"S3_upload_files"
        else:
            print(
                f"Bucket '{S3_name}' either does not exist or wasn't created through the CLI. Please try again.")


def list_S3_input():
    owner = input("Who is the owner of the instances you would like to list? ")
    return {
        "owner": owner
    },"list_S3"
