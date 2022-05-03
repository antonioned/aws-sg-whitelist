from requests import get
from botocore.exceptions import ClientError
import boto3

ec2 = boto3.client('ec2')

ip = get('https://ifconfig.co/ip').content.decode('utf8').strip()
sg_id = '__SECURITY_GROUP_ID__'
port = input('Enter port for access: ')
name = input('Enter your name: ')

def describe_sg_rules():
    try:
        response = ec2.describe_security_group_rules(
                    Filters=[
                        {
                            'Name': 'group-id',
                            'Values': [
                                sg_id,
                            ]
                        },
                    ]
                )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            print('Authentication failure: check your AWS cli setup.')
        elif e.response['Error']['Code'] == 'RequestExpired':
            print('Your AWS credentials have expired, please set them again.')
        else:
            print('Caught exception: {}'.format(e))

def check_rule_exists():
    try:
        for rules in describe_sg_rules()['SecurityGroupRules']:
                if 'Description' in rules:
                    desc = rules['Description']
                    if desc != None and name.casefold() in desc.casefold():
                        return rules['SecurityGroupRuleId']
    except ClientError as e:
            print('Caught exception: {}'.format(e))

def apply_rule():
    if check_rule_exists():
        ec2.modify_security_group_rules(
            GroupId=sg_id,
            SecurityGroupRules=[
                {
                    'SecurityGroupRuleId': check_rule_exists(),
                    'SecurityGroupRule': {
                        'CidrIpv4': '{}/32'.format(ip),
                        'IpProtocol': 'tcp',
                        'FromPort': int(port),
                        'ToPort': int(port),
                        'Description': '{} static IP address.'.format(name)
                    }
                },
            ]
        )
    else:
        ec2.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'FromPort': int(port),
                        'ToPort': int(port),
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': '{}/32'.format(ip),
                                'Description': '{} static IP address.'.format(name)
                            }
                        ]
                    }
                ]
            )

apply_rule()
print('\nSG rule applied!')