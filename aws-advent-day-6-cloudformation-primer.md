Amazon CloudFormation Primer
----------------------------

[Amazon CloudFormation (CFN)](http://aws.amazon.com/cloudformation/) is an AWS service which provides users with a way to describe the AWS resources they want created, in a declarative and re-usable fashion, through the use of simple JSON formatted text files. It supports a wide variety of AWS services, includes the ability to pass in user supplied paramaters, has a nice set of CLI tools, and a few handy functions you are able to use in the JSON files.

__Stacks__

CloudFormation starts with the idea of a _stack_. A stack is a JSON formatted file with the following attributes

* A template the stack will be based on
* A list of template parameters, user supplied inputs, such as a EC2 instance or VPC id
* An optional list of mappings which are used to lookup values, such as AMI ids for different regions
* An optional list of data tables used to lookup static configuration values (e.g. AMI names)
* The list of AWS resources and their configuration values
* A list of outputs, such as the id of an ELB instance that was created

A stack can be created using the [AWS Console](https://console.aws.amazon.com), the [CLI tools](http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html), or an [API library](http://aws.amazon.com/code). Stacks can be as re-usable or as monolithic as your choose to make them. A future post will cover some ideas on CFN stack re-usable, design goals, and driving CFN stacks with Boto, but this post is going to focus on getting you up and running with a simple stack and give you some jumping off points for further research on your own.

You're able to use templates to create new stacks or update existing stacks.

Cost
-------

CloudFormation itself [does not cost anything](http://aws.amazon.com/cloudformation/faqs/#18). You are charged the normal AWS costs for any resources created as part of creating a new stack or updating an existing stack. 

__It's important to note you're charged [a full hour for any resources costs](http://aws.amazon.com/cloudformation/faqs/#19), even if you're stack gets rolled back due to an error during stack creation.__

** _This can mean it could become costly if you're not careful while testing and building your templates and stacks._ **


Getting Started
---------------

We're going to assume you already have an AWS account and are familiar with editing JSON files.

To get started you'll need to install the [CFN CLI tools](http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/cfn-installing-cli.html).

Writing a basic template
------------------------

A __template__ is a JSON formatted text file. Amazon ends theirs with a _.template_, while I prefer to name mine _.json_ as, for naming and syntax highlighting reasons, but ultimately this is arbitrary.

A template begins with the _AWSTemplateFormatVersion_ and a _Description_, and must contain at least one _Resources_ block with a single _Resource_.

A most basic template only needs what is show below

<code>
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "basic template"

  "Resources" : {
    "Ec2Instance" : {
      "Type" : "m1.small",
      "Properties" : {
        "ImageId" : "ami-16fd7026",
      }
    }
  }
}
</code>

A template can contain _Parameters_ for user input. An example of this would be a parameter for the instance type. 

As you'll see in the example below, you refer to paramaters or other _values_ using a special function, called _Ref_.


<code>
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "basic template with instance parameter"

  "Parameters" : {
    "InstanceType" : {
    "Description" : "EC2 instance type",
    "Type" : "String",
  },

  "Resources" : {
    "Ec2Instance" : {
      "Type" : { "Ref" : "InstanceType"}
      "Properties" : {
        "ImageId" : "ami-16fd7026",
      }
    }
  }
}
</code>

Sometimes _Mappings_ are a better option than _Parameters_, a common pattern you'll see in CFN templates is using a Mapping for the AMI ids in various AWS rgions, as shown below

<code>
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "basic template with instance parameter"

  "Parameters" : {
    "InstanceType" : {
    "Description" : "EC2 instance type",
    "Type" : "String",
  },

  "Mappings" : {
    "RegionMap" : {
      "us-east-1"      : { "AMI" : "ami-7f418316" },
      "us-west-1"      : { "AMI" : "ami-951945d0" },
      "us-west-2"      : { "AMI" : "ami-16fd7026" },
      "eu-west-1"      : { "AMI" : "ami-24506250" },
      "sa-east-1"      : { "AMI" : "ami-3e3be423" },
      "ap-southeast-1" : { "AMI" : "ami-74dda626" },
      "ap-northeast-1" : { "AMI" : "ami-dcfa4edd" }
    }
  },


  "Resources" : {
    "Ec2Instance" : {
      "Type" : { "Ref" : "InstanceType"}
      "Properties" : {
        "ImageId" : { "Fn::FindInMap" : [ "RegionMap", { "Ref" : "AWS::Region" }, "AMI" ]},
      }
    }
  }
}
</code>


Where to go from here
---------------------

Amazon has provided a wide variety of templates in the [Sample Templates library](http://aws.amazon.com/cloudformation/aws-cloudformation-templates/), ranging from [single EC2 instances](), to [Drupal]() or [Redmine]() application stacks, and even a full blown [multi-tier application in a VPC](), which you're able to download and run.