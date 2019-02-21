# mini-nat-ami

## What is?

Automated creation of a minimal **AWS EC2 AMI** with **NAT** support.

## What for?

In the official **NAT** instance **AMI** provided by **AWS**,
the root **EBS** volume is **8GB** while the actual size of all files is well under **2GB**. 
Using standard methods it is not possible to decrease size of an **EBS** volume while keeping the entire file-system intact.

The code is also quite generic and can be adjusted to help with different use-cases.

## How to?
### Prepare
  - Install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) 
  - Install [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    - Make sure you also install [botocore](https://pypi.org/project/botocore/), [boto](https://pypi.org/project/boto/)
    and [boto3](https://pypi.org/project/boto3/)

### Configure AWS
  - Set up a user with access keys
  - Make sure the user can assume admin [[role]](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html)
    - Make sure the role requires MFA device, for example 
    [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)

In my case it looks similar to:

``` bash
# cat ~/.aws/credentials
[auto_admin]
aws_access_key_id = XXX
aws_secret_access_key = XXX 

# cat ~/.aws/config
[default]
region = eu-central-1

[profile auto_admin]
role_arn = arn:aws:iam::123456789012:role/admin_role_for_auto_admin
source_profile = auto_admin
mfa_serial = arn:aws:iam::123456789012:mfa/auto_admin
```

### Execute the playbooks

In the cloned directory of this repository:

```bash
# Make sure the top level variables look sensible
cat vars.yml
sed -i 's/123456789012/210987654321/' vars.yml

# Execute playbooks one by one
ansible-playbook sandbox_create_playbook.yml -e mfa_token=123456
ansible-playbook usecase_create_playbook.yml 
ansible-playbook usecase_test_playbook.yml 
ansible-playbook usecase_destroy_playbook.yml 
ansible-playbook sandbox_destroy_playbook.yml -e mfa_token=123456
```

## What if?
  - The code was created and tested on [Linux Mint](https://linuxmint.com/)
    - ansible 2.7.6
    - aws-cli/1.16.96 Python/2.7.15rc1 Linux/4.18.0-13-generic botocore/1.12.86
  - It exercises a somehow disputable trick of using an existing **mini-ami** and 
  overriding entire file-system except the old **Grub 0.97** in the **boot-record**
  - Here is a diagram depicting the flow:

![diagram](https://raw.githubusercontent.com/mkusanagi/mini-nat-ami/master/aws-packer-mini-nat-ami-ansible.png)
