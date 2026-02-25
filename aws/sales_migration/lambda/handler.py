import json
import boto3

s3_client = boto3.client("s3")

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

    # list all .done files currently in the raw bucket
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Suffix=".done"
    )

    done_files = [obj["Key"] for obj in response.get("Contents", [])]
    print(f"Done files found: {done_files}")

    # define which .done files we expect before proceeding
    expected_done_files = [
        "source_a.done",
        "source_b.done",
        "source_c.done"
    ]

    all_done = all(f in done_files for f in expected_done_files)

    if all_done:
        print("All sources ready. Triggering pipeline...")
        # next step will go here (Step Functions trigger)
    else:
        missing = [f for f in expected_done_files if f not in done_files]
        print(f"Still waiting for: {missing}")

    return {
        "statusCode": 200,
        "body": json.dumps({"all_done": all_done})
    }