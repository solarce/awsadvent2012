Options for Automating AWS
--------------------------

As we've seen in previous posts, [boto](https://github.com/boto/boto) and [cloudformation](http://aws.amazon.com/cloudformation/) are both options for helping automate your AWS resources, and can even compliment each other. 

But not everyone will want to use Amazon's CFN (which we covered in depth in the [day 6 post](http://awsadvent.tumblr.com/post/37251281257/getting-started-with-boto)) or a Python library, so I thought we'd explore some of the options for automating your usage of AWS in various programming languages.

Python - boto, libcloud
-----------------------

Python has a few options for libraries. The most actively developed and used one's I've seen are [boto](https://github.com/boto/boto) and [libcloud](http://libcloud.apache.org/)

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

Ruby - fog, aws-sdk gem
-----------------------

The main Ruby options seem to be [Fog](http://fog.io/1.8.0/index.html) and the [aws-sdk](http://aws.amazon.com/articles/8621639827664165) gem.

__Fog__

Similar to libcloud, Fog's goal is to a be a mature cloud provider library with support for many providers. It provides a Ruby interface to them, with AWS being one of the first it supported and among the most mature in those that Fog supports. It's also used to provide EC2 support for Opscode Chef's [knife](http://wiki.opscode.com/display/chef/Knife)

Fog is organized around four components

* Compute
* Storage
* CDN
* DNS

Based on a review of the [supported services list](http://fog.io/1.8.0/about/supported_services.html) and the [aws library code](https://github.com/fog/fog/tree/master/lib/fog/aws), Fog currently has support for all the major AWS services.

If you're interested in learning more about Fog, take a look at the [Getting Started tutorial](http://fog.io/1.8.0/about/getting_started.html) and the [source code](https://github.com/fog/fog)

__aws-sdk__

The aws-sdk gem is the official gem from Amazon that's meant to help Ruby developers integrate AWS services into their applications, with special support for Rails applications in particular.

It currently supports the following AWS services:

* Amazon Elastic Compute Cloud (EC2)
* Amazon SimpleDB (SDB)
* Amazon Simple Storage Service (S3)
* Amazon Simple Queue Service (SQS)
* Amazon Simple Notifications Service (SNS)

If you're interested in learning more about the ruby sdk, see the [Getting Started guide](http://aws.amazon.com/articles/8621639827664165) and the [FAQ](http://aws.amazon.com/sdkforruby/faqs/)

Java - jclouds, AWS SDK for Java
--------------------------------

The Java world has a number of options, including [jclouds](http://www.jclouds.org/) and the official [SDK for Java](http://aws.amazon.com/sdkforjava/)

__jclouds__

jclouds is a Java and Clojure library whose goal is to a be a mature cloud provider library with support for many providers. It provides a Java interface to them, with AWS being one of the first it supported and among the most mature in those that jclouds supports.

jclouds is organized into two main components

* Compute API
* Blobstore API

jclouds currently has support for the following AWS services

* EC2
* SQS
* EBS
* S3
* CloudWatch

__SDK for Java__

The SDK for Java is the official Java library from Amazon that's meant to help Java developers integrate AWS services into their applications.

It currently supports all the AWS services.

If you're interested in learning more about the Java sdk, see the [Getting Started guide](http://aws.amazon.com/articles/3586?_encoding=UTF8&jiveRedirect=1) and the [API documentation](http://docs.amazonwebservices.com/AWSJavaSDK/latest/javadoc/index.html)


PHP - AWS SDK for PHP
---------------------

The only PHP full featured PHP library I could find was the official [SDK for PHP](http://aws.amazon.com/sdkforphp/)

The SDK for PHP is the official PHP library from Amazon that's meant to help PHP developers integrate AWS services into their applications.

It currently supports all the AWS services.

If you're interested in learning more about the PHP sdk, see the [Getting Started guide](http://docs.amazonwebservices.com/AWSSdkDocsPHP/latest/DeveloperGuide/php-dg-setup.html) and the [API documentation](http://docs.amazonwebservices.com/AWSSDKforPHP/latest/)

JavaScript - AWS SDK for Node.JS, AWSLib
--------------------------------

There seem to be two JavaScript options, the [AWS SDK for Node.js](http://aws.amazon.com/sdkfornodejs/) and [aws-lib](https://github.com/livelycode/aws-lib)

__SDK for Node.js__

The SDK for Node.js is the official JavaScript library from Amazon that's meant to help Javascript and Node.js developers integrate AWS services into their applications. This SDK is currently considered a __developer preview__

It currently supports the following AWS services

* EC2
* S3
* DynamoDB
* Simple Workflow

If you're interested in learning more about the Node.js sdk, see the [Getting Started guide](http://docs.amazonwebservices.com/nodejs/latest/dg/nodejs-dg-aws-sdk-for-node.js.html) and the [API documentation](http://docs.amazonwebservices.com/AWSJavaScriptSDK/latest/frames.html)

__aws-lib__

aws-lib is a simple Node.js library to communicate with the Amazon Web Services API.

It currently supports the following services

* EC2
* Product Advertising API
* SimpleDB
* SQS (Simple Queue Service)
* SNS (Simple Notification Service)
* SES (Simple Email Service)
* ELB (Elastic Load Balancing Service)
* CW (CloudWatch)
* IAM (Identity and Access Management)
* CFN (CloudFormation)
* STS (Security Token Service)
* Elastic MapReduce

If you're interested in learning more about aws-lib, see the [Getting started page](http://livelycode.com/aws-lib/) and read the [source code](https://github.com/livelycode/aws-lib/tree/master/lib).



