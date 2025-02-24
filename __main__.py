import json
from EC2 import ec2
from S3 import S3
from Route53 import Route53

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

config = load_config()
congif_1 = config[1]
if congif_1=="crete_ec2" or congif_1=="two_instances":
    ec2.number_of_instances()
elif congif_1=="list_ec2":
    ec2.list_instances()
elif congif_1=="manage_ec2":
    ec2.manage_ec2()

elif congif_1=="create_S3":
    S3.create_S3()
elif congif_1=="S3_upload_files":
    S3.upload_files()
elif congif_1=="list_S3":
    S3.list_s3()

elif congif_1=="create_zone":
    Route53.create_zone()
elif congif_1=="manage_record":
    Route53.manage_dns_record()








