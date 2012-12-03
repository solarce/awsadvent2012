Some key AWS Concepts
=====================

To kick off AWS Advent 2012 we're going to take a tour of the main AWS concepts that people use.

Regions and Availability Zones
------------------------------

Regions are the top level __compartmentalization__ of AWS services. Regions are geographic locations in which you create and run your AWS resources. 

As of December 2012, there are currently [eight regions](http://aws.amazon.com/about-aws/globalinfrastructure/regional-product-services/)

* N. Virginia - us-east-1
* Oregon - us-west-2
* N. California - us-west-1
* Ireland - eu-west-1
* Singapore - ap-southeast-1
* Tokyo - ap-northeast-1
* Sydney - ap-southeast-2
* São Paulo - sa-east-1

Within a region there are multiple Availability Zones (AZ). An availability is analagous to a data center and your AWS resources of certain types, within a region, can be created in one or more availability zones to improve redundancy within a region.

AZs are designed so that networking between them is meant to be low latency and fairly reliable, but ideally you'll run your instances and services in multiple AZs as part of your architecture.

One thing to note about regions and pricing is that it will vary by region for the same AWS service. US-EAST-1 is by far the most popular region, as it was the lowest cost for a long time, so most services built in EC2 tend to run in this region. US-WEST-2 recently had it's EC2 cost set to match EAST-1, but not all services are available in this region at the same cost yet.


EC2
---------

EC2 is the [Elastic Compute Cloud](http://aws.amazon.com/ec2/faqs/#What_is_Amazon_Elastic_Compute_Cloud_Amazon_EC2). It provides you with a variety of [compute instances](http://aws.amazon.com/ec2/instance-types/) with CPU, RAM, and Disk allocations, on demand, and with [hourly based pricing](http://aws.amazon.com/ec2/pricing/) being the main way to pay for instanance, but you can also [reserve instances](http://aws.amazon.com/ec2/purchasing-options/).

EC2 instances are packaged as AMI (Amazon Machine Images) and these are the base from which your instances will be created. A number of [operating systems are supported](https://aws.amazon.com/amis), including Linux, Windows Server, FreeBSD (on some instance types), and OmniOS.


There are two types of instance storage available.

1. Ephemeral storage: Ephemeral storage is local to the instance host and the number of disks you get depends on the size of your instance. This storage is wiped whenever there is an event that terminates an instance, whether an EC2 failure or an action by a user.

2. Elastic Block Store (EBS): EBS is a separate AWS service, but one of it's uses is for the root storage of instances. These are called __EBS backed__ instances. EBS volumes are block devices of _N_ gigabytes that are available over the network and have some advanced snapshotting and performance features. This storage persists even if you terminate the instance, but this incurs additional costs as well. We'll cover more EBS details below. If you choose to use EBS optimized instance types, your instance will be provisioned with a dedicated NIC for your EBS traffic. Non-EBS optimized instanced share EBS traffic with all other traffic on the instance's primary NIC.

EC2 instances offer a number of useful feature, but it important to be aware that instances are not meant to be reliable, it is possible for an instance to go away at any time (host failure, network partitions, disk failure), so it is important to utilize instances in a redundant (ideally multi-AZ) fashion. 

S3
---------

S3 is the [Simple Storage Service](http://aws.amazon.com/s3/faqs/#What_is_Amazon_S3). It provides you with the ability to store objects via interaction with an HTTP API and have those objects be stored in a highly available way. You pay for objects stored in S3 based on [the total size of your objects, GET/PUT requests, and bandwidth transferred](http://aws.amazon.com/s3/#pricing).

S3 can be coupled with Amazon's CDN service, [CloudFront](), for a simple solution to object storage and delivery. You're even able to complete host a [static site](http://docs.amazonwebservices.com/AmazonS3/latest/dev/WebsiteHosting.html) on S3.

The main pitfalls of using S3 are that latency and response can vary, particularly with large files, as each object is stored synchronosly on multiple storage devices within the S3 service. Additionally, some organizations have found that S3 can become expensive for many terabytes of data and it was cheaper to bring in-house, but this will depend on your existing infrastructure outside of AWS.

EBS
---------

As previously mentioned, [EBS](http://aws.amazon.com/ebs/) is Amazon's Elastic Block Store service, it provides block level storage volumes for use with Amazon EC2 instances. Amazon EBS volumes provided over the network, and are persistant, independent from the life of your instance. An EBS volume is local to an availability zone and can only be attached to one instance at a time. You're able to take snapshots of EBS volumes for backups and cloning, that are persisted to S3. You're also able to create a __Provisioned IOPS volume__ that has guaranteed performance, for an additional cost. You pay for EBS volumes based on [the total size of the volume and per million I/O requests](http://aws.amazon.com/pricing/ebs/)

While EBS provides flexibility as a network block device and offers some compelling features with snapshotting and being persistant, its performance can vary, wildly at times, and unless you use EBS optimized instance types, your EBS traffic is shared with all other traffic on your EC2 instances single NIC. So this should be taken into consideration before basing important parts of your infrastructure on top of EBS volumes.

ELB
----------

ELB is the [Elastic Load Balancer](http://aws.amazon.com/elasticloadbalancing/) service, it provides you with the ability to load balance TCP and UDP services, with both IPv4 and IPv6 interfaces. ELB instances are local to a region and are able to send traffic to EC2 instances in multiple availability zones at the same time. Like any good load balancer, ELB instances are able to do sticky sessions and detect backend failures. When coupled with [CloudWatch](http://aws.amazon.com/cloudwatch/) metrics and an [Auto-Scaling Group](http://aws.amazon.com/autoscaling/), you're also able to have an ELB instance automatically create and stop additional EC2 instances based on a variety of performance metrics. You pay for ELB instances based on [each ELB instance running and the amount of data, in GB, transferred through each ELB instance](http://aws.amazon.com/pricing/elasticloadbalancing/)

While ELB offers ease of use and the most commonly needed features of load balancers, without the need to build your own load balancing with additional EC2 instances, it does add significant latency to your requests (often 50-100ms per request), and has been shown to be dependent on other services, like EBS, as the most recent issue in US-EAST-1 demonstrated. These should be taken into consideration when choosing to utilize ELB instances.

Authentication and Authorization
--------------------------------

As you've seen, any serious usage of AWS resources is going to cost money, so it's important to be able to control who within your organization can manage your AWS resources and affect your billing. This is done through Amazon's [Identity Access and Management (IAM)](http://aws.amazon.com/iam/) service. As the administrator of your organization's AWS account (or if you've been given the proper permissions via IAM), you're able to easily provide users with logins, API keys, and through a variety of security roles, let them manage resources in some or all of the AWS services your organization uses. As IAM is for managing access to your AWS resources, there is no cost for it.

Managing your AWS resources
---------------------------

Since AWS is meant to be use to dynamically create and destroy various computing resources on demand, all AWS services include [APIs](http://aws.amazon.com/documentation/) with [libraries available for most languages](http://aws.amazon.com/code/). 

But if you're new to AWS and want to poke around without writing code, you can use the [AWS Console](https://console.aws.amazon.com/console/home) to create and manage resources with a point and click GUI.

Other services
--------------

Amazon provides a [variety of other useful services](http://aws.amazon.com/products/) for you to build your infrastructure on top of. Some of which we will cover in more detail in future posts to [AWS Advent](http://awsadvent.tumblr.com/). Others we will not, but you can quickly learn about in the [AWS documentation](http://docs.amazonwebservices.com/).

A good thing to know is that all the AWS services are built from the same _primitives_ that you can use as the basis of your infrastructure on AWS, namely EC2 insances, EBS volumes, S3 storage.

Further reading
---------------

__EC2__

* [Getting Started](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
* [API](http://docs.amazonwebservices.com/AWSEC2/latest/APIReference/Welcome.html)
* [CLI](http://docs.amazonwebservices.com/AWSEC2/latest/CommandLineReference/Welcome.html)

__S3__

* [Getting Started](http://docs.amazonwebservices.com/AmazonS3/latest/gsg/GetStartedWithS3.html)
* [API](http://docs.amazonwebservices.com/AmazonS3/latest/API/)
* [Console](http://docs.amazonwebservices.com/AmazonS3/latest/UG/)

__EBS__

* [Getting Started](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/AmazonEBS.html)
* [API](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/ebs-api-cli-overview.html)

__ELB__

* [Getting Started](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/GettingStarted.html)
* [API](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/APIReference/Welcome.html)




