import logging
import pprint as p

import boto3

logging.basicConfig(level=logging.INFO)
session = boto3.Session()
client = session.client('config')
tag_client = session.client('resourcegroupstaggingapi')
# # session = boto3.Session()
vanta_tags = {
    "VantaDescription": "Cloud Infra managed resources",
    "VantaOwner": "Cloud Infra",
    "VantaNonProd": "true",
    "VantaContainsUserData": "false",
    "VantaUserDataStored": ""
}


# Returns a list of all the arns of each tagged resource
def all_tagged_resources(tag_client):
    # Initialize a session using DigitalOcean Spaces.
    all_resources = []
    # List all resources
    paginator = tag_client.get_paginator('get_resources')
    response_iterator = paginator.paginate()
    for response in response_iterator:
        for resource in response['ResourceTagMappingList']:
            all_resources.append(resource['ResourceARN'])
    logging.info(f"[+] Found {len(all_resources)} arns!")
    return all_resources


def tag_resources(arns):
    try:
        response = tag_client.tag_resources(ResourceARNList=arns,
                                            Tags=vanta_tags)
        logging.info(f"[+] Tagging Successful !")
        return response
    except Exception as e:
        logging.error(f"[!] Failed to tag {e}")


# Creates tags for Lambbda functions
def tag_lambdas():
    client = boto3.client('lambda')
    function_list = client.list_functions()
    functions = function_list.get('Functions')
    for func in functions:
        arn = func.get('FunctionArn')
        name = func.get('FunctionName')
        tags = client.list_tags(Resource=arn).get("Tags")
        if 'VantaContainsUserData' not in tags.keys():
            client.tag_resource(Resource=arn, Tags=vanta_tags)
            p.pprint(f"tags added to {name}")
        else:
            p.pp(f"Vanta tags found for {name}")


# Create Monitoring for all EC2 instances
# CPUUtilizatio

if __name__ == '__main__':
    arns = all_tagged_resources(tag_client)
    p.pp(tag_resources(arns))