from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class K8SVPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "k8s-vpc",
            cidr =  "10.0.0.0/16",
            max_azs = 2,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name = "public-subnet",
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 26
                ),
                ec2.SubnetConfiguration(
                    name = "private-subnet",
                    subnet_type = ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask = 26
                )
            ]
        )