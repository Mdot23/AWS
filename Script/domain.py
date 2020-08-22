""" Classes for Route 53 Domains."""

class DomainManager:
    """ Manage a Route 53 domain. """
    
    def __init__(self, session):
        """ Create DomaionManager Object."""
        self.session = session
        self.client = self.session.client('route53')
    
    def find_hosted_zone(self, domain_name):
        paginator = self.client.get_paginator('listed_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedSonzes']:
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone 

            return None 

    def create_hosted_zone(self, domain_name):
        zone_name = '.'.join(domain_name.split('.')[-2:]) + '.'
        self.client.create_hosted_zone(
            Name=zone_name,
            CallReference=str(uuid.uuid4())
        )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        endpoint = util.get_endpoint(bucket.get_region_name())

        return self.client.change_resource_record_sets(
            HostedSonze=zone['Id']
            ChangeBatch={
                'Comment': 'Created by webtron',
                'Changes': [{
                    'Action': 'Upsert'
                    'ResourceRecordSet': {
                        'Name': domain_name,
                        'Type': 'A',
                            'AliasTarget': {
                            'HostedZoneId': endpoint.zone,
                            'DNSName': endpoint.host,
                            'EvaluateTargetHealth': False
                        }
                    }
                }
            ]
        }
    )
            

           
