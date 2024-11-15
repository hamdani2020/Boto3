import uuid

import boto3

s3_resource = boto3.resource("s3")


def create_bucket_name(bucket_prefix):
    """
    Generates a unique bucket name by combining a given prefix with a UUID.

    Parameters:
        bucket_prefix (str): The prefix to be used at the beginning of the bucket name.

    Return:
        str: A unique bucket name with a specified prefix, ensuring the length is
        between 3 and 63 characters, as required for bucket naming conventions.
    """
    return "".join([bucket_prefix, str(uuid.uuid4())])


# s3_resource.create_bucket(Bucket=TEST_S3,
#                           CreateBucketConfiguration={
#                           'LocationConstraint': 'eu-west-2'
#                           })


def create_bucket(bucket_prefix, s3_connection):
    """
    Creates a unique bucket name combining the given prefix with UUID.

    parameters:
        bucket_prefix (str): The prefix to be given to generate the bucket name.
        s3_connection(boto3.client): Boto3 S3 client to interact with the AWS S3.

    Return:
        tuple: A tuple containing the bucket name and the response from the AWS
        service (dict) after the bucket name is created.
    """
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": current_region},
    )
    print(bucket_name, current_region)
    return bucket_name, bucket_response


first_bucket_name, first_response = create_bucket(
    bucket_prefix="hamdanibucket", s3_connection=s3_resource
)

print(first_bucket_name)


# Second Bucket
def create_bucket(bucket_prefix, s3_connection):
    """
    Creates a unique bucket name combining the given prefix with UUID.

    parameters:
        bucket_prefix (str): The prefix to be given to generate the bucket name.
        s3_connection(boto3.client): Boto3 S3 client to interact with the AWS S3.

    Return:
        tuple: A tuple containing the bucket name and the response from the AWS
        service (dict) after the bucket name is created.
    """
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": current_region},
    )
    print(bucket_name, current_region)
    return bucket_name, bucket_response


second_bucket_name, second_response = create_bucket(
    bucket_prefix="hamdanibucket", s3_connection=s3_resource
)

print(second_bucket_name)


def create_temp_file(size, file_name, file_content):
    """
    Creates a temporal file with specified size, file name suffix and sample of
    content to the file to be repeated.

    parameters:
        size (int): Number of repetitions of `file_content` to reach the desired the file size.
        file_name (str): Suffix for the file name.
        file_content (str): Content to be repeated in the file.

    Return:
        str: The name of the created temporal file.
    """
    random_file_name = "".join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, "w") as f:
        f.write(str(file_content) * size)
    return random_file_name


first_file_name = create_temp_file(300, "firstfile.txt", "f")
print(first_file_name)

# Bucket and Object instance
first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name)

# Sub-resouces (They are methods that create a new instance of a child resource)
first_object_again = first_bucket.Object(first_file_name)
first_bucket_again = first_object.Bucket()

# File upload to s3 using Object instance
s3_resource.Object(first_bucket_name, first_file_name).upload_file(
    Filename=first_file_name
)

# Downloading a file from s3
# s3_resource.Object(first_file_name, first_file_name).download_file(
#     f"/tmp/{first_file_name}"
# )


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {"Bucket": bucket_from_name, "Key": file_name}
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)


copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)


# Deleting object
s3_resource.Object(second_bucket_name, first_file_name).delete()
