# mk (c) 2019
# Remove user's section from aws credentials file
from configparser import ConfigParser

# Collect variables from ansible
iam_user_name = "{{ iam_user_name }}"
aws_credentials_file = "{{ aws_credentials_file }}"

# Load the aws credentials file
cp = ConfigParser()
cp.read(aws_credentials_file)

if cp.has_section(iam_user_name):
    cp.remove_section(iam_user_name)

    with open(aws_credentials_file, 'w') as cred:
        cp.write(cred)
