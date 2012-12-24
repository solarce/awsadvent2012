Strategies for re-usable CloudFormation Templates
-------------------------------------------------

In [day 7's post](http://awsadvent.tumblr.com/post/37391299521/cloudformation-primer) we learned about how [CloudFormation (CFN)](http://aws.amazon.com/cloudformation/) can help you to automate the creation and management of your AWS resources. It supports a wide variety of AWS services, includes the ability to pass in user supplied paramaters, has a nice set of CLI tools, and a few handy functions you are able to use in the JSON files.

In today's post we'll explore some strategies for getting the most out of your CFN stacks by creating re-usable templates.

Down with Monolithic
--------------------

A lot of the [CFN sample templates](http://aws.amazon.com/cloudformation/aws-cloudformation-templates/) are __monothithic__, meaning that the [template]() defines all the resources needed for an application's infrastructure in a single template and so they all get created as part of a single stack. Examples of this are the [Multi-tier VPC example](https://s3.amazonaws.com/cloudformation-templates-us-east-1/multi-tier-vpc.template) or the [Redmine Multi-AZ with Multi-AZ RDS example](https://s3.amazonaws.com/cloudformation-templates-us-east-1/Redmine_Multi_AZ.template).

In keeping with the ideas of [agile operations](http://www.slideshare.net/rsim/agile-operations-or-how-to-sleep-better-at-night) or [infrastructure as code](http://www.agileweboperations.com/the-implications-of-infrastructure-as-code), I think that the way we should use CFN templates is as re-usable bits of _infrastructure code_ to manage our AWS resources.

Layer cake
----------

The approach that I've come up with for this is a series of _layers_, as outlined below:

* [VPC]() template - this defines the VPC for a region, your set of subnets (private and public), an internet gateway, any NAT instances you may want, your initial security groups, and possibly network ACLs
* [EC2]() instance template - here you define the kinds of instances you want to run, passing in a VPC id, one or more AMI ids, security groups, EBS volumes, etc that are needed to run your infrastructure. Whether you make a template that is takes everything as parameters or one that is more monolithic in defining your instances is up to you
* [ELB]() (+ [Auto-scaling]()) template - this defines one or more ELB instances needed, passing in your EC2 instances ids, listener ports, subnets, etc as parameters. Optionally, if you're going to use auto-scaling, I'd include that in this template, along with the parameters needed it for it, since AS makes most sense when used with ELB for web facing applications.
* [S3]() (+ [CloudFront]()) template - this defines the buckets, ACLs, lifecycle policies, etc that are needed. Parameters
* [RDS]() template - this defines your RDS instances, taking a VPC id, subnet, RDS instance class, etc as parameters
* If you're using [Route53]() for DNS, I recommend putting the needed Route53 resources in each _layer_'s template.

These covers the most common resources you're likely to use in a typical web applications, if you're using other services like [Elastic Map Reduce]() or [Simple Notification Services]() then you should make additional templates as needed.

The overall approach is that your templates should have sufficient parameters and outputs to be re-usable across _environments_ like __dev__, __stage__, __qa__, or __prod__ and that each _layer_'s template builds on the next.

Some examples
-------------

As with any new technique, it is useful to have some examples.

__Example VPC template__

This template does not require any inputs, it will make a VPC with a network of _10.20.0.0/16_, a public subnet of _10.20.10.0/24_ , a private subnet of _10.20.20.0/24_, with default inbound 22 and 80 rules, and typical outbound rules.

It returns the newly created VPC's id.

<pre>

{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "Template to make VPC with private and public subnet",

  "Parameters" : {

  },

  "Resources" : {

    "VPC" : {
      "Type" : "AWS::EC2::VPC",
      "Properties" : {
        "CidrBlock" : "10.20.0.0/16",
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Public" }
        ]
      }
    },

    "VPCSecurityGroup" : {    
     "Type" : "AWS::EC2::SecurityGroup",
     "Properties" :
     {
      "GroupDescription" : "Enable SSH access via port 22",
      "SecurityGroupIngress" : [ {
        "IpProtocol" : "tcp",
        "FromPort" : "22",
        "ToPort" : "22",
        "CidrIp" : "0.0.0.0/0"
        } ],
      "VpcId" : { "Ref" : "VPC" }
     }
    },

    "PublicSubnet" : {
      "Type" : "AWS::EC2::Subnet",
      "Properties" : {
        "AvailabilityZone" : "us-west-2a",
        "VpcId" : { "Ref" : "VPC" },
        "CidrBlock" : "10.20.10.0/24",
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Public" }
        ]
      }
    },

    "InternetGateway" : {
      "Type" : "AWS::EC2::InternetGateway",
      "Properties" : {
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Public" }
        ]
      }
    },

    "AttachGateway" : {
       "Type" : "AWS::EC2::VPCGatewayAttachment",
       "Properties" : {
         "VpcId" : { "Ref" : "VPC" },
         "InternetGatewayId" : { "Ref" : "InternetGateway" }
       }
    },

    "PublicRouteTable" : {
      "Type" : "AWS::EC2::RouteTable",
      "Properties" : {
        "VpcId" : {"Ref" : "VPC"},
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Public" }
        ]
      }
    },

    "PublicRoute" : {
      "Type" : "AWS::EC2::Route",
      "Properties" : {
        "RouteTableId" : { "Ref" : "PublicRouteTable" },
        "DestinationCidrBlock" : "0.0.0.0/0",
        "GatewayId" : { "Ref" : "InternetGateway" }
      }
    },

    "PublicSubnetRouteTableAssociation" : {
      "Type" : "AWS::EC2::SubnetRouteTableAssociation",
      "Properties" : {
        "SubnetId" : { "Ref" : "PublicSubnet" },
        "RouteTableId" : { "Ref" : "PublicRouteTable" }
      }
    },

    "PublicNetworkAcl" : {
      "Type" : "AWS::EC2::NetworkAcl",
      "Properties" : {
        "VpcId" : {"Ref" : "VPC"},
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Public" }
        ]
      }
    },

    "InboundHTTPPublicNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PublicNetworkAcl"},
        "RuleNumber" : "100",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "false",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "80", "To" : "80"}
      }
    },

    "InboundDynamicPortsPublicNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PublicNetworkAcl"},
        "RuleNumber" : "101",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "false",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "1024", "To" : "65535"}
      }
    },

    "OutboundHTTPPublicNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PublicNetworkAcl"},
        "RuleNumber" : "100",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "true",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "80", "To" : "80"}
      }
    },

    "OutBoundDynamicPortPublicNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PublicNetworkAcl"},
        "RuleNumber" : "101",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "true",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "1024", "To" : "65535"}
      }
    },

    "PublicSubnetNetworkAclAssociation" : {
      "Type" : "AWS::EC2::SubnetNetworkAclAssociation",
      "Properties" : {
        "SubnetId" : { "Ref" : "PublicSubnet" },
        "NetworkAclId" : { "Ref" : "PublicNetworkAcl" }
      }
    },

    "PrivateSubnet" : {
      "Type" : "AWS::EC2::Subnet",
      "Properties" : {
        "AvailabilityZone" : "us-west-2a",
        "VpcId" : { "Ref" : "VPC" },
        "CidrBlock" : "10.20.30.0/24",
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Private" }
        ]
      }
    },

    "PrivateRouteTable" : {
      "Type" : "AWS::EC2::RouteTable",
      "Properties" : {
        "VpcId" : {"Ref" : "VPC"},
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Private" }
        ]
      }
    },

    "PrivateSubnetRouteTableAssociation" : {
      "Type" : "AWS::EC2::SubnetRouteTableAssociation",
      "Properties" : {
        "SubnetId" : { "Ref" : "PrivateSubnet" },
        "RouteTableId" : { "Ref" : "PrivateRouteTable" }
      }
    },

    "PrivateNetworkAcl" : {
      "Type" : "AWS::EC2::NetworkAcl",
      "Properties" : {
        "VpcId" : {"Ref" : "VPC"},
        "Tags" : [
          {"Key" : "Application", "Value" : { "Ref" : "AWS::StackName"} },
          {"Key" : "Network", "Value" : "Private" }
        ]
      }
    },

    "InboundPrivateNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PrivateNetworkAcl"},
        "RuleNumber" : "100",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "false",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "0", "To" : "65535"}
      }
    },

    "OutBoundPrivateNetworkAclEntry" : {
      "Type" : "AWS::EC2::NetworkAclEntry",
      "Properties" : {
        "NetworkAclId" : {"Ref" : "PrivateNetworkAcl"},
        "RuleNumber" : "100",
        "Protocol" : "6",
        "RuleAction" : "allow",
        "Egress" : "true",
        "CidrBlock" : "0.0.0.0/0",
        "PortRange" : {"From" : "0", "To" : "65535"}
      }
    },

    "PrivateSubnetNetworkAclAssociation" : {
      "Type" : "AWS::EC2::SubnetNetworkAclAssociation",
      "Properties" : {
        "SubnetId" : { "Ref" : "PrivateSubnet" },
        "NetworkAclId" : { "Ref" : "PrivateNetworkAcl" }
      }
    },

  "Outputs" : {
    "VPC-ID" : {
      "Value" : { "Ref" : "VPC" }
    }
  }
}
</pre>

__Example EC2 instance template__

This template will create an EC2 instance, it requires you give it an ssh keypair name, a VPC id, a Subnet id within your VPC, an AMI id, and a Security Group.

It returns the EC2 instance id, the subnet, and the security group id.

<pre>
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "make an instance, based on region, ami, subnet, and security group",

  "Parameters" : {

    "KeyName" : {
      "Description" : "Name of and existing EC2 KeyPair to enable SSH access to the instance",
      "Type" : "String"
    },

    "VpcId" : {
      "Type" : "String",
      "Description" : "VpcId of your existing Virtual Private Cloud (VPC)"
    },

    "SubnetId" : {
      "Type" : "String",
      "Description" : "SubnetId of an existing subnet in your Virtual Private Cloud (VPC)"
    },

    "AmiId" : {
      "Type" : "String",
      "Description" : "AMI You want to use"
      
    },

    "SecurityGroupId": {
      "Type" : "String",
      "Description" : "SecurityGroup to use"
    }

  },

  "Resources" : {

    "Ec2Instance" : {
      "Type" : "AWS::EC2::Instance",
      "Properties" : {
        "ImageId" : { "Ref" : "AmiId" },
        "SecurityGroupIds" : [{ "Ref" : "SecurityGroupId" }],
        "SubnetId" : { "Ref" : "SubnetId" },
        "KeyName" : { "Ref" : "KeyName" },
        "UserData" : { "Fn::Base64" : { "Fn::Join" : ["", [
          "#!/bin/bash -v\n",
          "curl http://chef-brentozar.s3.amazonaws.com/bootstrap.sh -o /tmp/bootstrap.sh\n",
          "bash /tmp/bootstrap.sh\n",
          "# If all went well, signal success\n",
          "cfn-signal -e $? -r 'Chef Server configuration'\n"
          ]]}}
      }
    }
  },

  "Outputs" : {
    "InstanceId" : {
      "Value" : { "Ref" : "Ec2Instance" },
      "Description" : "Instance Id of newly created instance"
    },

    "Subnet" : {
      "Value" : { "Ref" : "SubnetId" },
      "Description" : "Subnet of instance"
    },

    "SecurityGroupId" : {
      "Value" : { "Ref" : "SecurityGroupId" },
      "Description" : "Security Group of instance"
    }
  }

}
</pre>

Conclusion
----------

Hopefully this has provided you with some strategies and examples for how to create re-usable CFN templates and build your infrastructure from a series of layered stacks.

As you build your templates, you'll want to build some automation with a [language library]() to drive the creation of each stack and manage passing your inputs from one stack to the next or see the earlier AWS Advent post on [Automating AWS]().

To explore this further I recommend you play with and tear apart the [CloudFormation example templates]() Amazon has made available.




