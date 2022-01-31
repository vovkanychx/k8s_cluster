class SampleDatalakeFormationMainStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, props, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sourceBucket = self.node.try_get_context('datalake_source_bucket')
        # -----------------------------------------------------------------------------------------------------------------
        # NETWORK
        # -----------------------------------------------------------------------------------------------------------------
        vpc = _ec2.Vpc.from_lookup(self, id="sample_datalake_formation_vpc", vpc_id=self.node.try_get_context('network')['vpc_id'])

        dl_sg = _ec2.SecurityGroup(
                self,
                id="sample_datalake_formation_sg",
                vpc=vpc,
                security_group_name="sample_datalake_formation_sg"
        )
        for ip in self.node.try_get_context('network')['allowed_cidrs']:
            dl_sg.add_ingress_rule(
                peer=_ec2.Peer.ipv4(ip),
                connection=_ec2.Port.tcp(3306)
            )

        dl_sg.add_ingress_rule(
            peer = dl_sg,
            connection=_ec2.Port.all_traffic()
        )

        privateSubnets = vpc.private_subnets

        cdk.CfnOutput(self, 'VpcID', 
            description='Datalake VPC', 
            value=vpc.vpc_id, 
            export_name='VpcID')
        cdk.CfnOutput(self, 'SecurityGroupID', 
            description='Datalake Security Group', 
            value=dl_sg.security_group_id, 
            export_name='SecurityGroupID')

