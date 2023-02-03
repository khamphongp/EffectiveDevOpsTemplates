from troposphere import(

	Base64,
	ec2, 
	GetAtt,
	Join,
	Output, 
	Parameter,
	Ref,
	Template,
)

ApplicationPort = "3000"

# Create a new AWS CloudFormation template
t = Template()

""" Effective DevOps in AWS: HelloWorld web application"""

t.add_parameter(Parameter("KeyPair", 
	Description="Name of an exisitng EC2 KeyPair to SSH", 
	Type="AWS::EC2::KeyPair::KeyName",
	ConstraintDescription="Must be the name of an exsition EC2 KeyPair."
	))

t.add_resource(ec2.SecurityGroup(
	"SecurityGroup",
	GroupDescription="Allow SSH and TCP/{} access".format(ApplicationPort),
	SecurityGroupIngress=[
		ec2.SecurityGroupRule(
			IpProtocol="tcp",
			FromPort="22",
			ToPort="22",
			CidrIp="0.0.0.0/0",
		),
		ec2.SecurityGroupRule(
			IpProtocol="tcp",
			FromPort=ApplicationPort,
			ToPort=ApplicationPort,
			CidrIp="0.0.0.0/0",
		),
	],
))	

ud = Base64(Join('\n',[
	"#!/bin/bash",
	"sudo yum install --enablerepo=epel -y nodejs",
	"wget http://bit.ly/2vESNuc -o /home/ec2-user/helloworld.js",
	"wget http://bit.ly/2vVvT18 -o /etc/init/helloworld.conf",
	"start helloworld"
]))

t.add_resource(ec2.Instance(
	"instance",
	ImageId="ami-cfe4b2b0",
	InstanceType="t2.micro",
	SecurityGroups=[Ref("SecurityGroup")],
	KeyName=Ref("KeyPair"),
	UserData=ud,
))

t.add_output(Output(
	"WebUrl",
	Description="Application endpoint",
	Value=Join("", [
		"http://", GetAtt("instance", "PublicDnsName"),
		":", ApplicationPort
		]),
))

print (t.to_json())