import json
import boto3

s3_client = boto3.client("s3")
ssm_client = boto3.client("ssm")

def get_expected_files():
    """
    Fetch the expected .done files from SSM Parameter Store.
    This means we can update the list without touching the code.
    """
    response = ssm_client.get_parameter(
        Name="sales-migration-expected-done-files-bc"
    )
    return [f.strip() for f in response["Parameter"]["Value"].split(",")]

def lambda_handler(event, context):
    """
    Triggered when a file lands in the raw bucket.
    Checks if all expected .done files are present.
    If yes, triggers the next step in the pipeline.
    """
    # get the bucket and file that triggered this lambda
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"Triggered by: s3://{bucket}/{key}")

    # fetch expected files from parameter store
    expected_done_files = get_expected_files()
    print(f"Expecting: {expected_done_files}")

    # list all .done files currently in the raw bucket
    response = s3_client.list_objects_v2(Bucket=bucket)

    done_files = [
        obj["Key"] for obj in response.get("Contents", [])
        if obj["Key"].endswith(".done")
    ]

    all_done = all(f in done_files for f in expected_done_files)

    if all_done:
        print("All sources ready. Triggering pipeline...")
    else:
        missing = [f for f in expected_done_files if f not in done_files]
        print(f"Still waiting for: {missing}")

    return {
        "statusCode": 200,
        "body": json.dumps({"all_done": all_done})
    }
