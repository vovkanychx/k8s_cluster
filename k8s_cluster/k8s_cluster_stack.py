from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
)
from constructs import Construct

class K8SClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create k8s cluster
        k8s_cluster = eks.Cluster(self, "HelloEKS",
            version=eks.KubernetesVersion.V1_21,
            default_capacity=1
        )
        
        #create managed node group comprised spot instance
        k8s_cluster.add_nodegroup_capacity("managed-node-group",
            instance_types=[
                ec2.InstanceType("t2.micro")
            ],
            min_size=3,
            capacity_type=eks.CapacityType.SPOT
        )