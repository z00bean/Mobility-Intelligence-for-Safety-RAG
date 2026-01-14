import json
import boto3
sts = boto3.client("sts")
print("CALLER:", sts.get_caller_identity())

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Lambda reached successfully",
            "input": event.get("body")
        })
    }

