version = 0.1
[default.deploy.parameters]
stack_name = "hello"
resolve_s3 = true
s3_prefix = "hello"
region = "us-east-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []
profile = "admin"
