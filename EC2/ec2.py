import json
import boto3
import pulumi
import pulumi_aws as aws

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def number_of_instances():
    config = load_config()
    if config[1]=="two_instances":
        #create_ec2 function twice
        first_instance=config[0][0][0]
        second_instance=config[0][1][0]
        create_ec2(first_instance)
        create_ec2(second_instance)



def create_ec2(instance):
    config = load_config()

    # AMI IDs לפי סוג האינסטנס
    amazon_image_x86_64 = "ami-053a45fff0a704a47"  # Amazon Linux x86_64
    ubuntu_image_x86_64 = "ami-04b4f1a9cf54c11d0"  # Ubuntu x86_64

    amazon_image_arm64 = "ami-0c518311db5640eff"  # Amazon Linux ARM64
    ubuntu_image_arm64 = "ami-0a7a4e87939439934"  # Ubuntu ARM64

    if instance["instance_type"] == "t4g.nano":
        ami_id = amazon_image_arm64 if instance["ami_choice"] == "2" else ubuntu_image_arm64
    else:
        ami_id = amazon_image_x86_64 if instance["ami_choice"] == "2" else ubuntu_image_x86_64

    ec2_instance = aws.ec2.Instance(
        instance["name"],
        ami=ami_id,
        instance_type=instance["instance_type"],
        tags={
            "Name": instance["name"],
            "Owner": instance["owner"],
            "Platform": "CLI"
        }
    )

    pulumi.export("instance_id", ec2_instance.id)



def list_instances():
    config= load_config()
    instances = aws.ec2.get_instances(
        filters=[{
            "name": "tag:Platform",
            "values": ["CLI"]
        }, {
            "name": "tag:Owner",
            "values": [config[0]["owner"]]
        }]
    )

    print("Instances available:")
    for i, instance in enumerate(instances.ids):
        print(f"{i + 1}. Instance ID: {instance}")

    return instances.ids

# chat gpt says that the right one, check later

# import boto3
#
# def list_instances():
#     config = load_config()  # Make sure this function is defined elsewhere
#     ec2 = boto3.client('ec2')
#
#     # Get instances with the specified tags
#     response = ec2.describe_instances(
#         Filters=[
#             {
#                 "Name": "tag:Platform",
#                 "Values": ["CLI"]
#             },
#             {
#                 "Name": "tag:Owner",
#                 "Values": [config[0]["owner"]]
#             }
#         ]
#     )
#
#     # Collect instance IDs
#     instance_ids = []
#     for reservation in response["Reservations"]:
#         for instance in reservation["Instances"]:
#             instance_ids.append(instance["InstanceId"])
#
#     # Print the instances found
#     print("Instances available:")
#     for i, instance_id in enumerate(instance_ids):
#         print(f"{i + 1}. Instance ID: {instance_id}")
#
#     return instance_ids

def manage_ec2():
    config = load_config()

    if config[0]['instance_state'] == 'stop':
        ec2 = boto3.client('ec2')
        ec2.stop_instances(InstanceIds=[config[0]['instance_id']])
        print(f"Instance {config[0]['instance_id']} stopped.")

    elif config['instance_state'] == 'start':
        ec2 = boto3.client('ec2')
        ec2.start_instances(InstanceIds=[config[0]['instance_id']])
        print(f"Instance {config[0]['instance_id']} started.")
    else:
        print("Invalid action. Please choose 'start' or 'stop'.")

