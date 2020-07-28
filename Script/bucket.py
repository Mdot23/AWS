# =*= coding: utf-8 -*- 
from pathlib import Path 
import mimetypes 
import functools
import util
from botocore.exceptions import ClientError

from hashlibt import md5

"Classes for S3 Buckets."""

class BucketManager: 
    
    CHUNK_SIZE = 8388608

    """ Manage an S3 Bucket.""" 
    def __init__(self, session):
        """ Create a BucketManager object."""
        self.s3 = session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_chunksize=self.CHUNK_SIZE
        )
        self.mainfest = {}

    def get_region_name(self, bucket):
        "Get the buckets region name"
        bucket_location = self.s3.meta.client.get_bucket_location(Bucket=bucket.name)

        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """ Get website url """
        return "http://{}.{}".format(bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host)
            
        

    def all_buckets(self):
        """ Get an iterator for all buckets.""" 
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """ Get an iterator for all objects in bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        s3bucket = s3.create_bucket(Bucket=bucket_name)
        try:
           s3_bucket = self.s3.create_bucket(
               Bucket=bucket_name
            )
        except ClientError as e:
            if e.resposne['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error 

        return s3_bucket
    
    def set_policy(self, bucket):
        """ Set bucket policy to readable by everyone """ 
        policy = {
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*" %s3bucket
             ]
            }
          ]
        }  %bucket.name

        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        bucket.Website().put(WebsiteConfiguration={
         'ErrorDocument': {
         'Key': 'erro.html'
         },
        'IndexDocument': {
             'Suffix': 'index.html'
     }})
    
    def load_mainfest(self, bucket):
        """ Load mainfest for caching purposes."""
        paginator = s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.mainfest[obj['key']] = obj['Etag']
    
    @staticmethod
    def has_data(data):
        """ Generate md5 hash for data."""
        hash = md5
        hash.update(data)

        return hash 

    def gen_etag(self, file):
        """Generate etag for file."""
        hashes = [] 

        with (open(file, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)

                if not data:
                    break

                hashes.append(self.hash_data(data))

            if not hashes:
                return 

            elif len(hashes) == 1:
                return '"{}"'.format(hash.hexdigest())
            else:
                hash = self.hash_data(reduce(lambda x, y: x+ y, (h.digest()for h in hashes)))
                return '"{}-{}"'.format(hash.hexdigest(), len(hashes))

    @staticmethod   
    def upload_file(bucket, path, key):
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.gen_etag(path)
        if self.mainfest.get(key, '') == etag:
            return 


        return bucket.upload_file(
                path,
                key,
                ExtraArgs={
                        'ContentType': content_type
                },
                Config=self.transfer_config
        )

    def sync(self, pathname, bucket_name):
        bucket = self.s3.Bucket(bucket_name)
        self.load_mainfest(bucket)

        # Get full absolute path of directory 
        root = Path(pathname).expanduser().resolve()

        def perform_operation(target):
                for p in target.iterdir():
                        if p.is_dir(): 
                                perform_operation(p)
                        if p.is_file(): 
                                self.upload_file(bucket, str(p), str(p.relative_to(root)))

        perform_operation(root)
        
    








    


