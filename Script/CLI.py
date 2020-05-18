"""
Deploy websites with AWS for S3

Automates the process of deploying static websites for S3 
- Configure AWS S3 buckets 
  - Create them
  - Set them up for static web hosting 
  - Deploy local files to them 
"""

import boto3
import click
from bucket import BucketManager 

session = None
bucket_manager = None 

@click.group()
@click.option('--profile', default=None,
    help="Use a givne AWS profile.")
def cli(profile):
    # If profile name value, session config is assigned to that value 
    global session, bucket_manager 
    session_cfg = {}
    if profile:
            session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in bucket_manager.all_buckets():
        print(bucket.name)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    "List objects in a bucket"
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
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
    
    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
        "Sync contents of PATHANME to BUCKET"
        bucket_manager.sync(pathname, bucket)
        print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))
 
        
if __name__ == '__main__':
    cli()
