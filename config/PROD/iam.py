from awslambdacontinuousdelivery.tools.iam import (
    defaultAssumeRolePolicyDocument
  , oneClickCreateLogsPolicy
  )

from troposphere import Sub
from troposphere.iam import Role, Policy
from awacs.dynamodb import PutItem
import awacs.aws

def get_dynamoDB() -> Policy:
  statements = [
    awacs.aws.Statement(
      Action = [ PutItem ],
      Effect = awacs.aws.Allow,
      Resource = [ Sub("arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/IoTSensorDataPROD") ]
    )
  ]
  policyDoc = awacs.aws.Policy( Statement = statements )
  return Policy( PolicyName = Sub("DynamoDbPRODAccess-${AWS::StackName}")
               , PolicyDocument = policyDoc
               )

def get_iam(ref_name: str) -> Role:
  assume = defaultAssumeRolePolicyDocument("lambda.amazonaws.com")
  return Role( ref_name
             , RoleName = ref_name
             , AssumeRolePolicyDocument = assume
             , Policies = [ oneClickCreateLogsPolicy(), get_dynamoDB() ]
             )

if __name__ == "__main__":
  role = get_iam("Test")
  print(str(role.to_dict()))
