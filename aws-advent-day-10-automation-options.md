Options for Automating AWS
--------------------------

As we've seen in previous posts, [boto]() and [cloudformation]() are both options for helping automate your AWS resources, and can even compliment each other. 

But not everyone will want to use Amazon's CFN (which we covered in depth in the [day 6 post]()) or a Python library, so I thought we'd explore some of the options for automating your usage of AWS in various programming languages.

Python - boto, libcloud
-----------------------

Python has a few options for libraries. The most actively developed and used one's I've seen are [boto]() and [libcloud]()

__Boto__

Boto is meant to be a Python library for interacting with AWS service. It mirrors the AWS APIs in a Pythonic fashion and gives you the ability to build tools in Python on top of it, to manipulate and manage your AWS resources.

The project is lead by [Mitch Garnaat](https://twitter.com/garnaat), who is currently a Sr Engineer at Amazon.

Boto has a number of tutorials to get you started, including

* [EC2](http://boto.cloudhackers.com/en/latest/ec2_tut.html)
* [S3](http://boto.cloudhackers.com/en/latest/s3_tut.html) / [CloudFront](http://boto.cloudhackers.com/en/latest/cloudfront_tut.html)
* [VPC](http://boto.cloudhackers.com/en/latest/vpc_tut.html)
* [ELB](http://boto.cloudhackers.com/en/latest/elb_tut.html)

Currently the following AWS services are supported:

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

__libcloud__

libcloud is a mature cloud provider library that is an Apache project. It's meant to provide a Python interface to multiple cloud providers, with AWS being one of the first it supported and among the most mature in those that libcloud supports.

libcloud is organized around four components

* Compute - libcloud.compute.*
* Storage - libcloud.storage.*
* Load balancers - libcloud.loadbalancer.*
* DNS - libcloud.dns.*

Given the above components and my review of the API docs, libcloud effectively supports the following AWS services

* EC2
* S3 
* Route53

If you're interested in learning more about libcloud, take a look at the [Getting Started guide](http://libcloud.apache.org/getting-started.html) and the [API documentation](http://libcloud.apache.org/apidocs/0.11.4/)

Ruby - fog, awsgem, knife
-------------------------

The main Ruby options seem to be [Fog]() and the [aws-sdk](http://aws.amazon.com/articles/8621639827664165) gem, for libraries, and [Opscode Chef's]() [knife]() tool also has nice support for AWS (which is built on top of Fog).

__Fog__



__aws-sdk__





__knife__



Java - jclouds, AWS SDK for Java
--------------------------------

The Java world has a number of options, including [jclouds]() and the official [SDK for Java]()

http://aws.amazon.com/sdkforjava/

PHP - AWS SDK for PHP
---------------------

The only PHP full featured PHP library I could find was the official [SDK for PHP]()

http://aws.amazon.com/sdkforphp/

JavaScript - AWS SDK for Node.JS, AWSLib
--------------------------------

http://aws.amazon.com/sdkfornodejs/

https://github.com/livelycode/aws-lib
