import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='METheGreat93')
s3 = boto3.resource('s3')


@click.group()
def cli():
    pass


@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    "List objects in a bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"
    s3bucket = s3.create_bucket(Bucket='thegreatbucket23')

    try:
       s3_bucket = s3.create_bucket(
          Bucket=bucket
       )
    except ClientError as e:
        if e.resposne['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)


    policy = {
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*" %s3bucket
          ]
          }]} 

    pol = s3.BucketPolicy(s3bucket)
    return

    ws = s3Bucket.Website()
    ws.put(WebsiteConfiguration={
         'ErrorDocument': {
         'Key': 'erro.html'
         },
        'IndexDocument': {
             'Suffix': 'index.html'
     }})


if __name__ == '__main__':
    cli()
