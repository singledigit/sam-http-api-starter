#!/Users/ericdj/.pyenv/shims/python
import sys, json
import boto3

if len(sys.argv) == 1:
   print('CloudFormation stack required')
   sys.exit()

cloudformation_client = boto3.client('cloudformation')
lambda_client = boto3.client('lambda')

page = {}

# Grab stack from AWS
try:
    stack_resources = cloudformation_client.list_stack_resources(
        StackName=sys.argv[1]
    )
except Exception as e:
    print(e)
    sys.exit()

# Grab environment vars from each lambda in the stack
for resource in stack_resources['StackResourceSummaries']:
    if(resource['ResourceType']=='AWS::Lambda::Function'):
        lambda_config = lambda_client.get_function_configuration(
            FunctionName=resource['PhysicalResourceId']
        )
        if 'Environment' in lambda_config and 'Variables' in lambda_config['Environment']:
            page[resource['LogicalResourceId']] = lambda_config['Environment']['Variables']

# Print to console
print(json.dumps(page, indent=2))