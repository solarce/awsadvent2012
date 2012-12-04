Amazon Virtual Private Cloud
============================

Amazon Virtual Private Cloud (VPC) is a service which allows you to create an isolated, private network within an AWS region where you can run and use a variety of other AWS resources. You're able to create a variety of private IP space subnets and build routes and security policies between them to fully host a multi-tier application within AWS while maintaining isolation from other AWS customers.

How do I build a VPC?
=====================

A VPC is built from a number of parts

1. The VPC object: which you declare with a name and a broad private network space. (You can define 5 VPCs in a single region)
2. 1 or more subnets: which are segments of the VPC IP space
3. An Internet Gateway (IG): which connects your VPC to the public Internet via a NAT Instance
4. NAT Instance: an Amazon managed EC2 instance that provides NAT services to your VPC
5. Router: the router is a VPC service that performs routing between subnets with your user defined route tables

Optionally you can setup IPSec VPN tunnels which you terminate on your hardware in a DC or home network.

VPC supports four options for its network architecture.

1. VPC with a Public Subnet Only
2. VPC with Public and Private Subnets
3. VPC with Public and Private Subnets and Hardware VPN Access
4. VPC with a Private Subnet Only and Hardware VPN Access

AWS services you can use inside a VPC
=====================================

A number of AWS services provide you with instance based resources, and you're able to run those resources inside your VPC. These include

__ELB__

ELB instances are able to function inside VPCs in two ways

1. They are able to create interfaces inside your VPC subnets and then send traffic to EC2 instances inside your VPC
2. An ELB instance can be created with an internal IP in a VPC subnet. This is useful if for load balancing between internal tiers of your application architecture

__EC2__

All classes of EC2 instances are available to deploy inside your VPC.

Availability Zone placement of EC2 instances can be controlled by which subnet you place your EC2 instance(s) into.

__RDS__

All classes and types of RDS instances are available to deploy inside your VPC.

__Auto Scaling__

You're able to use Auto Scaling to scale EC2 instances inside your VPC, in conjunction with ELB instances.

Networking inside your VPC
==========================

Your VPC is divided into a set of subnets. 


# limitations
* need vpn (costs) or eip (costs) to get to instances 
* five vpc in a region

# cost
* a vpc is free
* subnets, security groups, acls are also free
