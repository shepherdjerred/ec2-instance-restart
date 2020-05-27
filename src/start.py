import boto3
import json
import os

region = "us-east-1"

instances = [os.environ["INSTANCEID"]]
secret = "SECRET"

def handler(event, context):
    request_secret = json.loads(event.get("body")).get("secret")
    if secret != request_secret:
        return json.dumps({ "message": "Authentication failed", "dump": event })

    ec2_client = boto3.client("ec2", region_name=region)
    ec2_client.start_instances(InstanceIds=instances)

    print(f"Started instances {str(instances)}")
    return json.dumps({ "message": "Instance Started" })
