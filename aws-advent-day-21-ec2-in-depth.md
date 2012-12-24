EC2 In-depth
------------

In day 1's post on [AWS Key Concepts](http://awsadvent.tumblr.com/post/37007485395/key-aws-concepts) we learned a little about [EC2](), but as you've come to see in these past few posts, anyone using seriously AWS is likely using EC2 as a major part of their application infrastructure.

Let's review what we learned about EC2 previously. EC2 is the [Elastic Compute Cloud](http://aws.amazon.com/ec2/faqs/#What_is_Amazon_Elastic_Compute_Cloud_Amazon_EC2). It provides you with a variety of [compute instances](http://aws.amazon.com/ec2/instance-types/) with set levels of CPU, RAM, and Disk allocations. You utilize these instances on demand, with [hourly based pricing](http://aws.amazon.com/ec2/pricing/), but you can also pay to [reserve instances](http://aws.amazon.com/ec2/purchasing-options/).

An EC2 instance operating system is cloned from an AMI (Amazon Machine Images). These are the base from which your instances will be created. A number of [operating systems are supported](https://aws.amazon.com/amis), including Linux, Windows Server, FreeBSD (on some instance types), and OmniOS.

__Pricing__

EC2 instance pricing is per hour and varies by instance type and class. You begin paying for an instance as soon as you launch it. You also pay AWS's typical bandwidth charges for any traffic that leaves the region your EC2 instance is running in.

For more details, consult the [EC2 FAQ on Pricing](http://aws.amazon.com/ec2/faqs/#How_will_I_be_charged_and_billed_for_my_use_of_Amazon_EC2).

Storage Options
---------------

There are two types of storage available for your instance's [root device volume](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/RootDeviceStorage.html):

1. Instance store: In this case the root device for an instance launched from the AMI is an instance store volume created from a template stored in Amazon S3. An instance store is not persistent and has a fixed size, but it uses storage local to the instance's host server. You're not able to derive new AMIs from instance store backed instances.

2. Elastic Block Store (EBS): EBS is a separate AWS service, but one of it's uses is for the root storage of instances. These are called __EBS backed__ instances. EBS volumes are block devices of _N_ gigabytes that are available over the network and have some advanced snapshotting and performance features. This storage persists even if you terminate the instance, but this incurs additional costs as well. We'll cover more EBS details below. If you choose to use EBS optimized instance types, your instance will be provisioned with a dedicated NIC for your EBS traffic. Non-EBS optimized instanced share EBS traffic with all other traffic on the instance's primary NIC.

There are also two types of storage available to instances for additional storage needs:


1. Ephemeral storage: Ephemeral storage are disks that are local to the instance host and the number of disks you get depends on the size of your instance. This storage is wiped whenever there is an event that terminates an instance, whether an EC2 failure or an action by a user.

2. EBS: As mentioned, EBS is a separate AWS service, you're able to create EBS volumes of _N_ gigabytes and attach them over the network. You're also able to take advantage ot their advanced snapshotting and performance features. This storage persists even if you terminate the instance, but this incurs additional costs as well.

Managing Instances
------------------

Managing instances can be done through the [AWS console](https://console.aws.amazon.com), the [EC2 API tools](http://aws.amazon.com/developertools/351), or the [API](http://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html) itself.

The lifecycle of a EC2 instance is typically

* [Creation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#EC2_LaunchInstance_Linux) from an AMI
* The instances runs, you may attach [EBS volumes] or [Elastic IPs], you may also restart the instance
* You may [stop]() an instance.
* Eventually you may [terminate]() the instance or the instance may go away due to a host failure.

It's important to note that EC2 instances are meant to be considered disposable and that you should use multiple EC2 instances in multiple _Availability Zones_ to ensure the availability of your applications.

Instance IPs and ENIs
---------------------

So once you've begun launching instances, you'll want to login and access them, and you're probably wondering what kind of IP addresses your instances come with.

The [EC2 FAQ on IP addresses](http://aws.amazon.com/ec2/faqs/#Why_am_I_limited_to_5_Elastic_IP_addresses) tells us:

> By default, every instance comes with a private IP address and an internet routable public IP address. The private address is associated exclusively with the instance and is only returned to Amazon EC2 when the instance is stopped or terminated. The public address is associated exclusively with the instance until it is stopped, terminated or replaced with an Elastic IP address.

If you're deploying your instances in a [VPC](http://aws.amazon.com/vpc/faqs/#G1), you're also able to use [Elastic Network Interfaces (ENIs)](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html). These are virtual network interfaces that let you add additional private IP addresses to your EC2 instances running in a VPC.

Security Groups
---------------

Ensuring your EC2 instances are secure at the network is a vital part of your infrastructure's overall security assurance. Network level security for EC2 instances is done through the use of [security groups](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html). 

A _security group_ acts as a firewall that controls the traffic allowed to reach one or more instances. When you launch an Amazon EC2 instance, you associate it with one or more security groups. You can add rules to each security group that control the inbound traffic allowed to reach the instances associated with the security group. All other inbound traffic is discarded. Security group rules are _stateful_.

Your AWS account automatically comes with a _default security group_ for your Amazon EC2 instances. If you don't specify a different security group at instance launch time, the instance is automatically associated with your default security group. 

The initial settings for the _default security group_ are:

* Allow no inbound traffic
* Allow all outbound traffic
* Allow instances associated with this security group to talk to each other

You can either chose to create new security groups with different sets of inbounds rules, which you'll need if you're running a multi-tier infrastructure, or you can [modify the default group](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html#distributed-firewall-example-default-group).

In terms of the limitations of security groups, you can create up to 500 Amazon EC2 security groups in each region in an account, with up to 100 rules per security group. In Amazon VPC, you can have up to 50 security groups, with up to 50 rules per security group, in each VPC. The Amazon VPC security group limit does not count against the Amazon EC2 security group limit.

Spot and Reserved Instances
---------------------------

Besides paying for EC2 instances on-demand, you're able to utilize instance capacity in two other ways, [Spot instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) and [Reserved instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts-on-demand-reserved-instances.html).

__Spot Instances__

If you have flexibility on when your application will run, you can bid on unused Amazon EC2 compute capacity, called Spot Instances, and lower your costs significantly. Set by Amazon EC2, the Spot Price for these instances fluctuates periodically depending on the supply of and demand for Spot Instance capacity.

To [use Spot Instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances-getting-started.html), you place a [Spot Instance request (your bid)](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances-bid-management.html) specifying the maximum price you are willing to pay per hour per instance. If the maximum price of your bid is greater than the current Spot Price, your request is fulfilled and your instances run until you terminate them or the Spot Price increases above your maximum price. Your instance can also be terminated when your bid price equals the market price, even when there is no increase in the market price. This can happen when demand for capacity rises, or when supply fluctuates.

You will often pay less per hour than your maximum bid price. The Spot Price is adjusted periodically as requests come in and the available supply of instances changes. Everyone pays that same Spot Price for that period regardless of whether their maximum bid price was higher, and you will never pay more than your hourly maximum bid price.

__Reserved Instances__

You can [use Reserved Instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-reserved-instances.html) to take advantage of lower costs by reserving capacity. With Reserved Instances, you pay a low, one-time fee to reserve capacity for a specific instance and get a significant discount on the hourly fee for that instance when you use it. Reserved Instances, which are essentially reserved capacity, can provide substantial savings over owning your own hardware or running only On-Demand instances. Reserved Instances are available from AWS in one- and three-year terms. Reserved Instances are available in three varieties—Heavy Utilization, Medium Utilization, and Light Utilization

Launching your Reserved Instance is the same as launching any On-Demand instance: You launch an instance with the same configuration as the capacity you reserved, and AWS will automatically apply the discounted hourly rate that is associated with your capacity reservation. You can use the instance and be charged the discounted rate for as long as you own the Reserved Instance. When the term of your Reserved Instance ends, you can continue using the instance without interruption. Only this time, because you no longer have the capacity reservation, AWS will start charging you the On-Demand rate for usage.

To purchase an Amazon EC2 Reserved Instance, you must select an instance type (such as m1.small), platform (Linux/UNIX, Windows, Windows with SQL Server), location (Region and Availability Zone), and term (either one year or three years). When you want your Reserved Instance to run on a specific Linux/UNIX platform, you must identify the specific platform when you purchase the reserved capacity.

Tagging
-------

[Tagging](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) is a minor EC2 feature that I find interesting. Tags are a key-value pair that you can apply to one or many EC2 instances. These let you add your own metadata to your EC2 instances for use in inventory or lifecycle management of your instances.

The following basic restrictions apply to tags:

* Maximum number of tags per resource—10
* Maximum key length—128 Unicode characters
* Maximum value length—256 Unicode characters
* Unavailable prefixes: aws (we have reserved it for tag names and values)
* Tag keys and values are case sensitive.

You're able to tag a [wide variety of resources](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html#resources-you-can-tag).

Tagging can be done through the [AWS console](https://console.aws.amazon.com), the [EC2 API tools](http://aws.amazon.com/developertools/351), or the [API](http://docs.aws.amazon.com/AWSEC2/latest/APIReference/Welcome.html) itself.

Conclusion
----------

EC2 instances are more than, but also different from, typical VPS instances. The flexibility of being able to use EC2 instances, of the many types and classes, coupled with the hourly pricing let's you do many things with your infrastructure that traditional data centers did not make possible. But the disposable nature of EC2 instances have some drawbacks. These should all be considered careful as you decide how and when to use EC2 instances for your applications.

As we've seen, there are a number of options for how you can pay for your EC2 instances and how you manage the instance lifecycle.

