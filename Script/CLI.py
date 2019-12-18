import boto3
import click
from botocore.exceptions import ClientError
from pathlib import Path 
import mimetypes 

session = boto3.Session(profile_name='Basic_User')
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
    s3bucket = s3.create_bucket(Bucket='webs2019')

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
   

    ws = s3Bucket.Website()
    ws.put(WebsiteConfiguration={
         'ErrorDocument': {
         'Key': 'erro.html'
         },
        'IndexDocument': {
             'Suffix': 'index.html'
     }})
    
    return

def upload_file(s3_bucket, path, key):
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        s3_bucket.upload_file(
                path,
                key,
                ExtraArgs={
                        'ContentType': 'text/html'
                })
@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
        "Sync contents of PATHANME to BUCKET"
        s3_bucket = s3.Bucket(bucket)
        # Get full absolute path of directory 
        root = Path(pathname).expanduser().resolve()

        def perform_operation(target):
                for p in target.iterdir():
                        if p.is_dir(): perform_operation(p)
                        if p.is_file(): upload_file(s3_bucket, str(p), str(p.relative_to(root)))

        perform_operation(root)
        
        
if __name__ == '__main__':
    cli()
