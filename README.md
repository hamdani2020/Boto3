# AWS S3 Bucket Management

This module provides functionality for managing AWS S3 buckets, including creating buckets, uploading files, copying between buckets, and cleaning up resources.

## Prerequisites

- AWS credentials properly configured
- Python 3.x
- Required packages:
  - `boto3`
  - `uuid`

## Core Functions

### `create_bucket_name(bucket_prefix)`

Generates a unique S3 bucket name by combining a prefix with a UUID.

**Parameters:**

- `bucket_prefix` (str): Prefix to be used at the start of the bucket name

**Returns:**

- str: A unique bucket name that follows AWS naming conventions (3-63 characters)

### `create_bucket(bucket_prefix, s3_connection)`

Creates a new S3 bucket with a unique name in the current AWS region.

**Parameters:**

- `bucket_prefix` (str): Prefix for the bucket name
- `s3_connection` (boto3.resource): Boto3 S3 resource object

**Returns:**

- tuple: (bucket_name, bucket_response)
  - `bucket_name` (str): Name of the created bucket
  - `bucket_response` (dict): AWS API response from bucket creation

### `create_temp_file(size, file_name, file_content)`

Creates a temporary file with specified content for testing uploads.

**Parameters:**

- `size` (int): Number of times to repeat the file_content
- `file_name` (str): Suffix for the generated file name
- `file_content` (str): Content to be repeated in the file

**Returns:**

- str: Name of the created temporary file

### `copy_to_bucket(bucket_from_name, bucket_to_name, file_name)`

Copies an object from one S3 bucket to another.

**Parameters:**

- `bucket_from_name` (str): Source bucket name
- `bucket_to_name` (str): Destination bucket name
- `file_name` (str): Name of the file to copy

## Usage Examples

### Creating Buckets

```python
s3_resource = boto3.resource("s3")
bucket_name, response = create_bucket("mybucket", s3_resource)
```

### Creating and Uploading Files

```python
# Create a temporary file
file_name = create_temp_file(300, "test.txt", "content")

# Upload file to S3
s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name)
```

### Working with Bucket and Object Instances

```python
# Get bucket instance
bucket = s3_resource.Bucket(name=bucket_name)

# Get object instance
obj = s3_resource.Object(bucket_name=bucket_name, key=file_name)

# Alternative way using sub-resources
obj_again = bucket.Object(file_name)
bucket_again = obj.Bucket()
```

### Copying Between Buckets

```python
copy_to_bucket(source_bucket, destination_bucket, file_name)
```

### Deleting Objects

```python
s3_resource.Object(bucket_name, file_name).delete()
```

## Important Notes

1. **Region Configuration**: The code uses the current region from the AWS session. Make sure your AWS credentials are configured for the desired region.

2. **Bucket Naming**:

   - Bucket names must be globally unique across all AWS accounts
   - Names must be between 3 and 63 characters long
   - Can only contain lowercase letters, numbers, dots, and hyphens

3. **Error Handling**:

   - The code assumes proper AWS credentials are configured
   - No explicit error handling is implemented - consider adding try/except blocks for production use

4. **Resource Cleanup**:
   - Remember to delete objects and buckets when they're no longer needed to avoid unnecessary charges
   - The code includes functionality to delete objects but not buckets

## Security Considerations

1. Ensure AWS credentials are properly secured and never committed to version control
2. Consider implementing bucket policies and access controls
3. Use appropriate IAM roles and permissions
4. Consider enabling bucket encryption for sensitive data

## Best Practices

1. Always clean up temporary files after uploading to S3
2. Implement proper error handling for production use
3. Consider implementing retry logic for AWS operations
4. Use bucket lifecycle policies for managing object retention
5. Consider implementing logging for tracking operations
