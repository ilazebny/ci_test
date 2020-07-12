#!/usr/bin/env python

import argparse
import boto3
import yaml


def parseCommandLine():
    parser = argparse.ArgumentParser(
        description='Get cloudformation stack outputs.')
    parser.add_argument('stackName',
                        help='name of stack to get outputs')
    parser.add_argument('-f', '--file',
                        help='yaml file to save outputs')
    parser.add_argument('-r', '--region', default='us-east-1',
                        help='AWS region to connect')
    args = parser.parse_args()
    return args


args = parseCommandLine()

client = boto3.client('cloudformation',  region_name=args.region)
response = client.describe_stacks(
    StackName=args.stackName,
    NextToken='string'
)

values = {}
for stack in response["Stacks"]:
    if stack["StackName"] == args.stackName:
        for output in stack["Outputs"]:
            values[output["OutputKey"]] = output["OutputValue"]

print(yaml.dump(values, default_flow_style=False))
if args.file:
    outfile = open(args.file, 'w')
    yaml.dump(values, outfile, default_flow_style=False)
