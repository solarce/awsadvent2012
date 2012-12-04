Amazon Virtual Private Cloud
----------------------------

Amazon Virtual Private Cloud (VPC) is a service which allows you to create an isolated, private network within an AWS region where you can run and use a variety of other AWS resources. You're able to create a variety of private IP space subnets and build routes and security policies between them to fully host a multi-tier application within AWS while maintaining isolation from other AWS customers.

How do I build a VPC?
---------------------

A [VPC](http://aws.amazon.com/vpc/faqs/) is built from a number of parts

1. The VPC object: which you declare with a name and a broad private network space. (You can define 5 VPCs in a single region)
2. 1 or more subnets: which are segments of the VPC IP space
3. An Internet Gateway (IG): which connects your VPC to the public Internet via a NAT Instance
4. NAT Instance: an Amazon managed EC2 instance that provides NAT services to your VPC
5. Router: the router is a VPC service that performs routing between subnets with your user defined route tables

Optionally you can setup [IPSec VPN tunnels](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_VPN.html) which you terminate on your hardware in a DC or home network.

VPC supports four options for its network architecture.

1. VPC with a Public Subnet Only
2. VPC with Public and Private Subnets
3. VPC with Public and Private Subnets and Hardware VPN Access
4. VPC with a Private Subnet Only and Hardware VPN Access

[Further Reading](http://docs.amazonwebservices.com/AmazonVPC/latest/GettingStartedGuide/GetStarted.html)

AWS services you can use inside a VPC
-------------------------------------

A number of AWS services provide you with instance based resources, and you're able to run those resources inside your VPC. These include

__ELB__

ELB instances are able to function inside VPCs in two ways

1. They are able to create interfaces inside your VPC subnets and then send traffic to EC2 instances inside your VPC
2. An ELB instance can be created with an internal IP in a VPC subnet. This is useful if for load balancing between internal tiers of your application architecture

[Further Reading](http://aws.amazon.com/ec2/faqs/#ELB8)

__EC2__

All classes of EC2 instances are available to deploy inside your VPC.

Availability Zone placement of EC2 instances can be controlled by which subnet you place your EC2 instance(s) into.

[Further Reading](http://aws.amazon.com/vpc/faqs/#E1)

__RDS__

All classes and types of RDS instances are available to deploy inside your VPC.

[Further Reading](http://aws.amazon.com/rds/faqs/#What_is_VPC_and_why_may_I_want_to_use_with_Amazon_RDS)

__Auto Scaling__

You're able to use Auto Scaling to scale EC2 instances inside your VPC, in conjunction with ELB instances.

[Further Reading](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_AutoScaling.html)

Networking inside your VPC
--------------------------

Your VPC is divided into a set of subnets. You control traffic between subnets and to the Internet with two necessary things and one optional. 

The required things are [route tables](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_Route_Tables.html) and [security groups](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html). 

A route table defines a subnet and a destination, which can be an instance ID, a network interface ID, or your Internet gateway.

A security group acts like a firewall and is associated with a set of EC2 instances. You define two sets of rules, based on TCP/UDP/ICMP and ports, one for ingress traffic and one for egress traffic. Security group rules are stateful.

Optionally, you can use [Network ACLs](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_ACLs.html)to control your TCP/UDP/ICMP traffic flow at the subnet layer. Rules defined in Network ACLs are not stateful, as so your rules must match up for ingress and egress traffic of a given service (e.g. TCP 22/SSH) to function.

[Further Reading](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_Security.html#VPC_Security_Comparison)

Some limitations of using VPCs
------------------------------

As with any product, VPC comes with some limitations. These include:

* You can only create five VPCs in a single AWS region
* You need to create a [VPN tunnel](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_VPN.html) or attach an [Elastic IP (EIP)](http://docs.amazonwebservices.com/AmazonVPC/latest/UserGuide/VPC_ElasticNetworkInterfaces.html) to get to instances, each if which has associated costs.
* You can only create 20 subnets per VPC
* You can only create 1 Internet Gateway per VPC

[Further Reading](http://aws.amazon.com/vpc/faqs/#Q2)

Cost
--------

Your VPC(s) do not cost anything to create or run. Additionally, subnets, security groups, and network ACLs are also free.

There will be costs associated with how you choose to access your instances inside your VPC, be that a VPN solution or using Elastic IPs.

All other AWS services cost the same whether you run those instances inside a VPC or outside.

[Further Reading](http://aws.amazon.com/vpc/faqs/#B1)

Summary
--------


In summary, VPCs provide an easy way to isolate application infrastructure, while still using a variety of AWS resources. With a little additional configuration, you're able to take advantage of the VPC service.
