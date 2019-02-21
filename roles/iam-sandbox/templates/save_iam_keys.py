# mk (c) 2019
# A quick workaround for ansible not returning the secret_access_key
import boto3
from configparser import ConfigParser

# Collect variables from ansible
admin_access_key = "{{ sts.sts_creds.access_key }}"
admin_secret_key = "{{ sts.sts_creds.secret_key }}"
admin_session_token = "{{ sts.sts_creds.session_token }}"

new_iam_user_name = "{{ iam_user_name }}"
aws_credentials_file = "{{ aws_credentials_file }}"

# Load the aws credentials file
cp = ConfigParser()
cp.read(aws_credentials_file)

if cp.has_section(new_iam_user_name):
    # If the credentials for the user are already there print them (for ansible)
    print(cp.get(new_iam_user_name, 'aws_access_key_id'))
    print(cp.get(new_iam_user_name, 'aws_secret_access_key'))
else:
    # If credentials are not there, create them, print and save
    session = boto3.Session(
        aws_access_key_id = admin_access_key,
        aws_secret_access_key = admin_secret_key,
        aws_session_token= admin_session_token
    )
    
    iam = session.resource('iam')
    user = iam.User(new_iam_user_name)
    access_key_pair = user.create_access_key_pair()

    print(access_key_pair.access_key_id)
    print(access_key_pair.secret_access_key)

    cp.add_section(new_iam_user_name)
    cp.set(new_iam_user_name, 'aws_access_key_id', access_key_pair.access_key_id)
    cp.set(new_iam_user_name, 'aws_secret_access_key', access_key_pair.secret_access_key)

    with open(aws_credentials_file, 'w') as cred:
        cp.write(cred)
