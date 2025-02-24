import json
from EC2 import EC2_input
from S3 import S3_input
import Route53
from Route53 import Route53_input


# Ask user to select action by number

print("Welcomr to Tohar's CLI!")
service=input("What service would you ike to use?\n  (1) EC2\n  (2) S3\n  (3) Route53 ")
if service == '1':
    user_action = input("Please enter the action you would like to perform\n  (1) Create\n  (2) List\n  (3) Manage ")
    # Perform action based on the user's choice
    if user_action == '1':
        with open("config.json", "w") as config_file:
            json.dump(EC2_input.number_of_instances_input(), config_file)

    elif user_action == '2':
        with open("config.json", "w") as config_file:
            json.dump(EC2_input.list_instance_input(), config_file)

    elif user_action == '3':
        with open("config.json", "w") as config_file:
            json.dump(EC2_input.instance_manage_user_input(), config_file)

    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if service == '2':
    user_action = input("Please enter the action you would like to perform\n  (1) Create S3\n  (2)  Upload Files to bucket\n  (3) List Buckets ")
    if user_action == '1':
        with open("config.json", "w") as config_file:
            json.dump(S3_input.create_S3_input(), config_file)
    if user_action =='2':
        with open("config.json", "w") as config_file:
            json.dump(S3_input.S3_upload_files_input(), config_file)
    if user_action =='3':
        with open("config.json", "w") as config_file:
            json.dump(S3_input.list_S3_input(), config_file)


if service == '3':
    user_action = input("Please enter the action you would like to perform\n  (1) Create DNS Zone\n  (2)  Manage DNS record ")
    if user_action == '1':
        with open("config.json", "w") as config_file:
            json.dump(Route53_input.create_zone_input(), config_file)
    if user_action =='2':
        with open("config.json", "w") as config_file:
            json.dump(Route53_input.manage_record_input(), config_file)

print("\n \n \ngreat!\nTo finalize your request, run\n\033[32m'pulumi up'\033[0m\nin your terminal\n")
print("if you would like to take more actions, run\n\033[32m'python get_user_input.py'\033[0m\nin your terminal ")
print("\033[34m!!! please make sure you run 'pulumi up' first to save your previous actions !!\033[0m")
print("Thank you for using Tohar's CLI!")










