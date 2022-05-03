# aws-sg-whitelist
Simple python script to update a security group in AWS with a whitelisted IP address.

## Prerequisites
- python3 & pip3,
- boto3 (pip3 install boto3)

## Setup
Clone the repo locally and `cd` into it. Before you run the script, set the AWS credentials locally, in the terminal
- export AWS_PROFILE=PROFILE_NAME

After this, edit the `whitelist.py` file to change the `sg_id` variable with the needed ID of the security group you need to whitelist your IP in.

## Usage
After editing the script is done, just run it with `python3 whitelist.py`. The script is interactive and it will prompt you to add the port you need access to and your name. **Your name is used in the sg rule description so that when added, you know exactly whose IP is that. Also, it plays a vital role in a check that checks if you already have an IP whitelisted. If yes, it will just update that one with the new IP instead of just repeatedly adding new IP addresses.**

## What is covered
- First IP whitelist (with description)
- Consecutive IP changes (when dynamic IP changes) based on the description/name check

## Contrubution
Feel free to fork the repo and create a PR!