import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm

class AwsCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(self,bucket_name="sales-migration-raw-bc")


