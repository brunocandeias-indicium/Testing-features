import json
import boto3
from sales_migration.handlers.done_file_handler import lambda_handler

def simulate(done_files_present):
    """
    Simulates an S3 event triggering the Lambda.
    done_files_present: list of .done files to pretend are in the bucket.
    """

    # first, upload the simulated .done files to the real raw bucket
    s3_client = boto3.client("s3")
    bucket = "sales-migration-raw-bc"

    # clear the bucket first
    response = s3_client.list_objects_v2(Bucket=bucket)
    for obj in response.get("Contents", []):
        s3_client.delete_object(Bucket=bucket, Key=obj["Key"])
        print(f"Cleared: {obj['Key']}")

    # upload the .done files we want to simulate
    for f in done_files_present:
        s3_client.put_object(Bucket=bucket, Key=f, Body=b"done")
        print(f"Uploaded: {f}")

    # build a fake S3 event (same structure AWS would send)
    fake_event = {
        "Records": [{
            "s3": {
                "bucket": {"name": bucket},
                "object": {"key": done_files_present[-1]}
            }
        }]
    }

    print("\n--- Lambda executing ---")
    result = lambda_handler(fake_event, context=None)
    print(f"\nResult: {result}")


if __name__ == "__main__":
    # scenario 1 - only 2 of 3 files present
    print("=== SCENARIO 1: Incomplete ===")
    simulate(["source_a.done", "source_b.done"])
    print("=== SCENARIO 1: Incomplete ===")
    print("\n=== SCENARIO 2: All files present ===")
    simulate(["source_a.done", "source_b.done", "source_c.done"])
    print("\n=== SCENARIO 2: All files present ===")


    print("\n=== SCENARIO 2: All files present ===")
    simulate(["source_a.done", "source_b.done", "source_a.done","source_b.done","source_c.done"])
    print("\n=== SCENARIO 2: All files present ===")