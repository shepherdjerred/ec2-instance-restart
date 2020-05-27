import boto3
import json
import os

region = "us-east-1"

instance = os.environ["INSTANCE_ID"]
secret = os.environ["SECRET"]


def handler(event, context):
    if "body" not in event:
        return json.dumps({
            "statusCode": 400,
            "body": "Bad request."
        })

    json_body = json.loads(event["body"])
    if "secret" not in json_body:
        return json_body({
            "statusCode": 401,
            "body": "No secret sent."
        })

    if secret != json_body["secret"]:
        return json.dumps({
            "statusCode": 401,
            "body": "Authentication failed."
        })

    try:
        ec2_client = boto3.client("ec2", region_name=region)
        ec2_client.stop_instances(InstanceIds=[instance])
    except Exception as e:
        return json.dumps({
            "statusCode": 500,
            "body": {
                "message": "Error when stopping instance",
                "details": str(e)
            }
        })

    return json.dumps({
        "statusCode": 200,
        "body": f"Instance {instance} Stopped"
    })
