import re
import boto3
from botocore.exceptions import ClientError

def is_valid_ec2_name(name):
    # Check length of the name
    if not (1 <= len(name) <= 128):
        print("Name must be between 1 and 128 characters.\nTry again")
        return False

    # Check for invalid characters using regex
    if not re.match(r'^[A-Za-z0-9\-_\.\s]+$', name):
        print("Name contains invalid characters. Only letters, numbers, hyphens, underscores, periods, and spaces are allowed.\nTry again")
        return False

    # Check if it starts or ends with invalid characters
    if name[0] in [' ', '.', '-'] or name[-1] in [' ', '.', '-']:
        print("Name cannot start or end with a space, period, or hyphen.\nTry again")
        return False

    print("Name is valid.")
    return True




def check_instance_exists(instance_id):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')

    try:
        # Describe the instance by ID
        response = ec2_client.describe_instances(InstanceIds=[instance_id])

        # Check if the instance exists
        if response['Reservations']:
            print(f"Instance {instance_id} exists.")

            # Get the tags of the instance
            tags = response['Reservations'][0]['Instances'][0].get('Tags', [])

            # Check if the instance has the required tag
            for tag in tags:
                if tag['Key'] == 'Platform' and tag['Value'] == 'CLI':
                    print(f"Instance {instance_id} has the tag platform=CLI.")
                    return True

            print(f"Instance {instance_id} does not have the tag platform=CLI.")
            return False

        else:
            print(f"Instance {instance_id} does not exist.")
            return False

    except ClientError as e:
        # Handle errors such as if the instance does not exist
        error_code = e.response['Error']['Code']
        if error_code == 'InvalidInstanceID.NotFound':
            print(f"Instance {instance_id} does not exist.")
        else:
            print(f"An error occurred: {e}")
        return False

def ec2_create_input():
    # שואל את המשתמש את השאלות
    name = input("The name of your instance: ")
    valid_ec2 = is_valid_ec2_name(name)
    while valid_ec2 == False:
        name = input("The name of your instance: ")
        valid_ec2 = is_valid_ec2_name(name)

    # שאלת סוג האינסטנס – המשתמש יבחר מספר 1 או 2
    print("What type of instance would you like to create?")
    print("1 - t3.nano")
    print("2 - t4g.nano")
    instance_type = input("Choose 1 or 2: ")

    # הגבלת סוגי אינסטנסים - לוודא שהמשתמש בחר 1 או 2
    while instance_type not in ["1", "2"]:
        print("Invalid input. Please choose 1 for t3.nano or 2 for t4g.nano.")
        instance_type = input("Choose 1 or 2: ")

    # אם המשתמש בחר 1, נבחר "t3.nano", אחרת "t4g.nano"
    instance_type = "t3.nano" if instance_type == "1" else "t4g.nano"

    # שאלת סוג ה-AMI – המשתמש יבחר מספר 1 או 2
    print("What type of AMI would you like to select?")
    print("1 - Latest Ubuntu")
    print("2 - Latest Amazon Linux AMI")
    ami_choice = input("Choose 1 or 2: ")

    # הגבלת סוגי AMI
    while ami_choice not in ["1", "2"]:
        print("Invalid input. Please choose 1 for Ubuntu or 2 for Amazon Linux.")
        ami_choice = input("Choose 1 or 2: ")

    # אם המשתמש בחר 1, נבחר "Ubuntu", אחרת "Amazon Linux"
    ami_choice = "1" if ami_choice == "1" else "2"

    owner = input("Who is the owner of this instance? (e.g., 'toharbarazi'): ")
    return {
        "name": name,
        "instance_type": instance_type,
        "ami_choice": ami_choice,
        "owner": owner
    },

def number_of_instances_input():
    number_of_instances=input("How many instances would you like to create? 1 / 2")
    while number_of_instances not in ["1", "2"]:
        print("Invalid input. You can create up to 2 instances")
        instance_type = input("Choose 1 or 2: ")

    if number_of_instances=='1':
        values=ec2_create_input()
        return values,"crete_ec2"
    else:
        instances_information=[]
        for i in range (2):
            print(f"\nPlease enter information about instance number {i+1}: ")
            values = ec2_create_input()
            instances_information.append(values)
        return instances_information,"two_instances"


def list_instance_input():
    owner = input("Who is the owner of the instances you would like to list? ")
    return {
        "owner": owner
    },"list_ec2"


def instance_manage_user_input():
    owner = input("Who is the owner of this instance? ")
    action = input("Please enter the action you would like to perform (start/stop): ")
    while action not in ['start','stop']:
        print("invalid action. Please choose between start or stop")
        action = input("invalid action. Please insert start or stop ")

    instance_id = input("Please enter the instance id to perform the action on: ")
    existing_instant=check_instance_exists(instance_id)
    while existing_instant==False:
        instance_id = input(f"instant doesnt exist.Please enter instance id to {action}: ")
        existing_instant = check_instance_exists(instance_id)


    return {
        "owner": owner,
        "instance_state": action,
        "instance_id": instance_id
    },"manage_ec2"
