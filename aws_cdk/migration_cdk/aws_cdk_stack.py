import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from aws_cdk import aws_events as event
from aws_cdk import aws_events_targets as target_event
from aws_cdk import aws_lambda as lambda_

import aws_cdk.aws_lambda as lambda_

class AwsCdkStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #### buckets ####
        
        raw_bucket = s3.Bucket(self,id = "Bucket_raw" ,bucket_name="sales-migration-raw-bc2")
        staging_bucket = s3.Bucket(self,id = "Bucket_staged" ,bucket_name="sales-migration-staged-bc2")
        
        
        #### event bridge + lambda ####
        
        fn = lambda_.Function(self, "donefile_handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="done_file_handler.lambda_handler",
            code=lambda_.Code.from_asset("lambda"))

        rule_donefile = event.Rule(self, 
                'event_rule_donefile', 
                event_pattern = event.EventPattern(
                    source=['aws.s3'],
                    detail_type=["Object Created"],
                    detail={"bucket": {
                "name": ["sales-migration-raw-bc2"]}}
                ))
        
        rule_donefile.add_target(target_event.LambdaFunction(fn))

        #### SSM ####

        #ssm_raw = ssm.StringParameter(self,"RawBucketNameParam", raw_bucket.bucket_name)

                #### event bridge + lambda ####
        

