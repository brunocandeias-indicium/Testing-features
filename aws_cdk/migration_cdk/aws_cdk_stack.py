import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_events as event

class AwsCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        raw_bucket = s3.Bucket(self,id = "Bucket_raw" ,bucket_name="sales-migration-raw-bc2")
        staging_bucket = s3.Bucket(self,id = "Bucket_staged" ,bucket_name="sales-migration-staged-bc2")

        event_rule_donefile = event.Rule(self, 
                                         'event_rule_donefile', 
                                         event_pattern = event.EventPattern(source=['aws.s3']))

        #ssm_raw = ssm.StringParameter(self,"RawBucketNameParam", raw_bucket.bucket_name)
        