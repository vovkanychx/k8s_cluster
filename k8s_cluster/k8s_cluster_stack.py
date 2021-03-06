from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam
)
from constructs import Construct

class K8SClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #use existing vpc
        vpc = ec2.Vpc.from_lookup(self, id = "eks-vps-id", 
            vpc_id = self.node.try_get_context('network')['vpc_id'])

        # create eks admin role
        admin_user = iam.User(self, "eks-admin-user")
        eks_master_role = iam.Role(self, 'eks-master-role',
            role_name = 'eks-admin-role',
            assumed_by = iam.AccountRootPrincipal()
        )

        #create k8s cluster
        k8s_cluster = eks.Cluster(self, "eks-cluster",
            version = eks.KubernetesVersion.V1_21,
            cluster_name = "my-eks-cluster",
            vpc = vpc, #vpc must run subnets in atleast 2 different AZs
            vpc_subnets = [ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)],
            default_capacity = 0,
            masters_role = eks_master_role,
            default_capacity_type = eks.DefaultCapacityType.NODEGROUP
        )

        k8s_cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])
        
        #create managed node group comprised spot instance
        k8s_cluster.add_nodegroup_capacity("managed-node-group",
            nodegroup_name = "eks-node-group",
            instance_types = [
                ec2.InstanceType("t2.micro")
            ],
            subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            max_size = 1,
            min_size = 1,
            desired_size = 1,
            capacity_type = eks.CapacityType.SPOT
        )