import json
import pulumi
import pulumi_aws as aws
import boto3

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)


def create_zone():
    config = load_config()


    public_zone = aws.route53.Zone(
        "examplePublicZone",
        name=config["name"],
        comment="Created by Tohar's CLI",
        tags={
            "Platform": "CLI"
        },
        # Disable the automatic creation of records if possible
        #force_destroy = True
    )


def create_record(zone_id,record_type,record_name,record_value,ttl):
    if not isinstance(record_value, list):
        record_value = [record_value]

    record = aws.route53.Record(
        record_name,
        zone_id=zone_id,
        name=record_name,
        type=record_type,
        ttl=ttl,
        records=record_value  # Directly use record_value list
    )
    pulumi.export(f"{record_name}_record", record)
    print(f"Successfully created record: {record_name}")

import boto3
from botocore.exceptions import ClientError

def delete_record(zone_id, record_type, record_name, record_value, ttl):
    if not isinstance(record_value, list):
        record_value = [record_value]

    route53_client = boto3.client('route53')
    change_batch = {
        'Changes': [
            {
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type,
                    'TTL': ttl,
                    'ResourceRecords': [{'Value': value} for value in record_value]  # Correct list format
                }
            }
        ]
    }

    try:
        response = route53_client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch=change_batch
        )
        print(f"Successfully deleted record: {record_name}")
    except ClientError as e:
        error_message = str(e)
        if "InvalidChangeBatch" in error_message and "not found" in error_message:
            # If the error is related to the record not being found, we can ignore it
            print(f"Record {record_name} was not found, skipping deletion. This is not an issue.")
        else:
            # For any other errors, re-raise it
            print(f"Error deleting record {record_name}: {e}")
            raise e


def manage_dns_record():
    """Manage DNS record based on the loaded configuration."""
    # Load configuration directly inside the function
    config = load_config()
    # Ensure record_value is always a list, even if it's a single string
    if isinstance(config[2], str):
        zone_id = config[0]["zone_id"]
        record_type = config[0]["record_type"]
        record_name = config[0]["record_name"]
        record_value = config[0]["record_value"]
        ttl = config[0]["ttl"]

        if not all([zone_id, record_type, record_name, record_value, ttl]):
            raise ValueError("Missing required configuration fields")

        if config[2]=="create":
            create_record(zone_id, record_type, record_name, record_value, ttl)
        else:
            delete_record(zone_id, record_type, record_name, record_value, ttl)

    else:
        #action is update
        #delete previous record
        zone_id = config[0]["zone_id"]
        record_type = config[0]["record_type"]
        record_name = config[0]["record_name"]
        record_value = config[0]["record_value"]
        ttl = config[0]["ttl"]

        if not all([zone_id, record_type, record_name, record_value, ttl]):
            raise ValueError("Missing required configuration fields")

        delete_record(zone_id, record_type, record_name, record_value, ttl)

        zone_id = config[2]["zone_id"]
        record_type = config[2]["record_type"]
        record_name = config[2]["record_name"]
        record_value = config[2]["record_value"]
        ttl = config[2]["ttl"]

        if not all([zone_id, record_type, record_name, record_value, ttl]):
            raise ValueError("Missing required configuration fields")

        create_record(zone_id, record_type, record_name, record_value, ttl)

