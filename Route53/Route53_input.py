import boto3
# import types_of_records
import sys
import os
sys.path.append(os.path.dirname(__file__))
import types_of_records
from botocore.exceptions import ClientError


def create_zone_input():
    name=input("Name your zone: ")
    return {
        "name": name
    },"create_zone"

def create_or_delete_record_input (zone_id):
    while True:
        record_type = input("Enter record type (A, CNAME, MX, TXT, AAAA): ").upper()
        valid_record_types = [
            "A", "AAAA", "CNAME", "MX", "TXT",
            "PTR", "SRV", "SPF", "NAPTR", "CAA",
            "DS", "TLSA", "SSHFP", "HTTPS", "SVCB"
        ]

        if record_type not in valid_record_types:
            print("Invalid record type. Please enter 'A', 'AAAA', 'CNAME', 'MX', 'TXT', 'PTR', 'SRV', 'SPF', 'NAPTR', 'CAA', 'DS', 'TLSA', 'SSHFP', 'HTTPS', or 'SVCB'.")
            continue

        record_name = input("Enter record name (e.g., www.example.com): ")
        if not record_name:
            print("Record name cannot be empty. Please try again.")
            continue

        # Step 6: Get and validate record value
        record_value = input(f"Enter record value for {record_type} record: ")

        # Validation based on record type
        record_value=types_of_records.record_types_conditions(record_type,record_value)

        # Validation of ttl
        ttl=types_of_records.valid_ttl()

        # After everything is validated, return the values in a dictionary
        return {
            "zone_id": zone_id,
            "record_type": record_type,
            "record_name": record_name,
            "record_value": record_value,
            "ttl": ttl
        }


import boto3
from botocore.exceptions import ClientError

def check_record_exists(record_data):
    # Initialize the Route 53 client
    route53_client = boto3.client('route53')

    try:
        # Get all records in the hosted zone with pagination
        paginator = route53_client.get_paginator('list_resource_record_sets')
        page_iterator = paginator.paginate(
            HostedZoneId=record_data['zone_id']
        )

        for page in page_iterator:
            for record in page['ResourceRecordSets']:
                # Normalize the record name by stripping the trailing dot
                record_name = record['Name'].lower().strip().rstrip('.')
                record_type = record['Type'].strip()
                record_ttl = record.get('TTL', None)
                record_values = [r['Value'].strip('"').strip() for r in record.get('ResourceRecords', [])]

                # Compare name, type, and TTL, then check if value exists
                if (record_name == record_data['record_name'].lower().strip().rstrip('.') and
                        record_type == record_data['record_type'].strip() and
                        (record_ttl == record_data['ttl'] or (record_ttl is None and record_data['ttl'] is None)) and
                        record_data['record_value'].strip() in record_values):
                    print("Record exists in the zone.")
                    return True

        print("Record does not exist in the zone.")
        return False

    except ClientError as e:
        print(f"An error occurred: {e}")
        return False





def manage_record_input():
    # Initialize the Route 53 client
    route53_client = boto3.client('route53')

    while True:
        # Step 1: Get and validate zone_id
        zone_id = input("Enter the Route 53 zone_id: ")

        try:
            # Fetch the tags for the zone
            response_tags = route53_client.list_tags_for_resource(
                ResourceType='hostedzone', ResourceId=zone_id
            )
            tags = response_tags.get('ResourceTagSet', {}).get('Tags', [])

            # Check if the 'Platform' tag exists and equals 'CLI'
            platform_tag_found = False
            for tag in tags:
                if tag.get('Key') == 'Platform' and tag.get('Value') == 'CLI':
                    platform_tag_found = True
                    break

            if not platform_tag_found:
                print(f"Zone {zone_id} does not have the 'Platform' tag with value 'CLI'. Please provide a valid zone_id.")
                continue

            print(f"Zone {zone_id} is valid and has the 'Platform' tag with value 'CLI'.")

            # Step 2: Fetch the records in the hosted zone
            response_records = route53_client.list_resource_record_sets(HostedZoneId=zone_id)
            records = response_records.get('ResourceRecordSets', [])
            print("Records in the hosted zone:")
            for record in records:
                print(f"Record Name: {record['Name']}, Record Type: {record['Type']}")

        except route53_client.exceptions.NoSuchHostedZone as e:
            print(f"Invalid zone_id: {zone_id}. Error: {str(e)}. Please try again.")
            continue
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")
            continue

        # Step 3: Get and validate action
        action = input("Enter action (create/update/delete): ").lower()
        if action not in ["create", "update", "delete"]:
            print("Invalid action. Please enter 'create', 'update', or 'delete'.")
            continue

        if action == "create":
            action=create_or_delete_record_input(zone_id)
            return action,"manage_record","create"

        elif action == "delete":
            action=create_or_delete_record_input(zone_id)
            record_exist=check_record_exists(action)
            while record_exist== False:
                print("try again")
                action = create_or_delete_record_input(zone_id)
                record_exist = check_record_exists(action)



            return action,"manage_record","delete"

        elif action == "update":
            print("\n \nprocess of updating record:\n  (1)information about original version of record\n  please make sure you insert the right values of the record\n  (2)information about new version of record\n  You can make any changes you'd like at the same time!")
            print("Let's start!")
            print("Insert information about original version of record:\n ")
            original=create_or_delete_record_input(zone_id)
            record_exist = check_record_exists(original)
            while record_exist == False:
                print("try again")
                original = create_or_delete_record_input(zone_id)
                record_exist = check_record_exists(original)
            #original and delete
            print("\n \nGreat! now Insert information about new version of record:\n ")
            new=create_or_delete_record_input(zone_id)
            return original,"manage_record",new


        # All inputs are valid now, so break out of the loop
        print(f"Valid inputs received. Proceeding with the action: {action} record.")
        break

# manage_record_input()
# with open("config.json", "w") as config_file:
#     json.dump(manage_record_input(), config_file)