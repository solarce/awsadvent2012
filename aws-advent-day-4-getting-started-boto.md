Getting Started with Boto
-------------------------

[Boto](https://github.com/boto/boto) is a Python library that provides you with an easy way to interact with and automate using various Amazon Web Services.

If you're familiar with Python or interested in learning it, in conjunction with learning and use AWS, you won't find a better option than Boto.

Installing
----------

Installing boto is very straightforward, assuming your using an OS with [pip](http://www.pip-installer.org/) installed. If you do not currently have pip, then [do that first](http://www.pip-installer.org/en/latest/installing.html).

Once you have pip, the following command will get you up and running.

`pip install boto`

Basic configuration
-------------------

This configuration assumes you've already created an AWS account and obtained your [API Key](http://docs.amazonwebservices.com/IAM/latest/UserGuide/IAM_Concepts.html#ConceptsAWSEntities) and [Secret Access Key](http://docs.amazonwebservices.com/IAM/latest/UserGuide/IAM_Concepts.html#ConceptsAWSEntities) from [IAM](http://docs.amazonwebservices.com/IAM/latest/UserGuide/Welcome.html) in the [AWS console](https://console.aws.amazon.com/console/default)

With those in hand, you'll want to create a [.boto file](http://docs.pythonboto.org/en/latest/boto_config_tut.html) in your home directory and populate it with the secrets. 

* Example _.boto_:

	`[Credentials]`

	`aws_access_key_id = <your access key>`

	`aws_secret_access_key = <your secret key>`

* There are some additional configurations you can set, as needed, for debugging, local proxies, etc, as shown below

	`[Boto]`

	`debug = 0`
	
	`num_retries = 10`

	`proxy = myproxy.com`

	`proxy_port = 8080`
	
	`proxy_user = foo`
	
	`proxy_pass = bar`

Using boto with EC2
-------------------

Now that you have a basic [.boto file](http://docs.pythonboto.org/en/latest/boto_config_tut.html), you can begin using boto with AWS resources.

The most likely place to start is connecting to [EC2](http://docs.pythonboto.org/en/latest/ec2_tut.html) and making an instance, which can be done with a few short lines of code.

_simple-ec2.py_

`import boto.ec2`

`regions = boto.ec2.regions()`

`oregon = regions[4]`

`# known from looking at regions[]`

`e = boto.ec2.EC2Connection(region=oregon)`

`# EC2Connection() will pick up your keys from .boto`

`conn.run_instances('<ami-image-id>')`

You can also specify a number of options to the AMI you're launching.

_options-ec2.py_

`import boto.ec2`

`regions = boto.ec2.regions()`

`oregon = regions[4]`

`# known from looking at regions[]`

`e = boto.ec2.EC2Connection(region=oregon)`

`# EC2Connection() will pick up your keys from .boto`

`conn.run_instances('<ami-image-id>'`

`      key_name='myKey',`

`      instance_type='c1.xlarge',`

`      security_groups=['your-security-group-here'])`

The [EC2 API](http://docs.pythonboto.org/en/latest/ref/ec2.html) has a number of options and function calls you will find useful in managing your EC2 resources with boto.

Using boto with VPC
-------------------

EC2 isn't the only service boto supports, one of my favorites, [VPC](http://docs.pythonboto.org/en/latest/vpc_tut.html) is also supported.

With a few short lines of code, you can create a VPC and its various objects.

_vpc.py_

`# this will create a VPC, a single subnet, and attach an internet gateway to the VPC`

`import boto.vpc`

`regions = boto.ec2.regions()`

`oregon = regions[4]`

`# known from looking at regions[]`

`v = boto.vpc.VPCConnection(region=oregon)`

`vpc = v.create_vpc('10.20.0.0/24')`

`subnet = v.create_subnet(vpc.id, '10.20.10.0/24')`

`ig = v.create_internet_gateway()`

`v.attach_internet_gateway(ig, vpc.id)`

The [VPC API](http://docs.pythonboto.org/en/latest/ref/vpc.html#) has a number of options and function calls you will find useful in managing your EC2 resources with boto.

What AWS resources are supported?
---------------------------------

A variety of services are supported. According to the boto [README](https://github.com/boto/boto/blob/develop/README.rst), they are currently

Compute

* Amazon Elastic Compute Cloud (EC2)
* Amazon Elastic Map Reduce (EMR)
* AutoScaling
* Elastic Load Balancing (ELB)

Content Delivery

* Amazon CloudFront

Database

* Amazon Relational Data Service (RDS)
* Amazon DynamoDB
* Amazon SimpleDB

Deployment and Management

* AWS Identity and Access Management (IAM)
* Amazon CloudWatch
* AWS Elastic Beanstalk
* AWS CloudFormation

Application Services

* Amazon CloudSearch
* Amazon Simple Workflow Service (SWF)
* Amazon Simple Queue Service (SQS)
* Amazon Simple Notification Server (SNS)
* Amazon Simple Email Service (SES)

Networking

* Amazon Route53
* Amazon Virtual Private Cloud (VPC)

Payments and Billing

* Amazon Flexible Payment Service (FPS)

Storage

* Amazon Simple Storage Service (S3)
* Amazon Glacier
* Amazon Elastic Block Store (EBS)
* Google Cloud Storage

Workforce

* Amazon Mechanical Turk

Other

* Marketplace Web Services

Automating with boto
--------------------

As you can see from the examples above, you can very quickly begin automating your AWS resources with boto. 

As you learn boto there are a number of resources to consult.

1. There are a number of [Tutorials](http://docs.pythonboto.org/en/latest/) for some services to help you get started
2. The [API documentation] is very comprehensive.
3. I find [bpython](http://bpython-interpreter.org/screenshots/) to be very helpful, as it's autocompletion makes it easily to quickly and interactively learn new parts of a library. [Obligatory bpython and boto action shot](http://bits.inatree.org/images/3._bpython_%28Python%29-20121120-152539.jpg)
4. Reading the [boto source code](https://github.com/boto/boto/tree/develop/boto). Never underestimate the power of just going to the source. Looking under the hood and seeing how things are put together can be very valuable and educational.
5. Join the community. [#boto](irc://irc.freenode.net:6667/boto) on freenode and the [google group](https://groups.google.com/forum/?fromgroups#!forum/boto-users) are both excellent places to start.






