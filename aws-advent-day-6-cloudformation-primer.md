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

_basic.template_
<code>
</code>

A template can contain _Parameters_ for user input. An example of this would be a parameter for the instance type. 

As you'll see in the example below, you refer to paramaters or other _values_ using a special function, called _Ref_.

_basic-paramater.template_
<code>
</code>

Sometimes _Mappings_ are a better option than _Parameters_, a common pattern you'll see in CFN templates is using a Mapping for the AMI ids in various AWS rgions, as shown below

_basic-mapping.template_
<code>
</code>

Finally, you're usually going to want to use one or more _Outputs_ in your template to provide you with information about the resources the creation of stack made.

_basic-output.template_
<code>
</code>

Once you've created a template, you'll want to validate that it works with the _cfn-validate-template_ command from the CLI tools.

An example of using it with a local file is shown below

`cfn-validate-template --template-file basic-output.template`

`PARAMETERS  InstanceTypeInput  false  EC2 instance type`

After you've verified the template is valid, you can try creating it using the _cfn-create-stack_ command. The you give the command a _stackname_ and a file or URL for the template you want to use. The command will return some info, including the new stack id 

Note:__Running this command with a template will create AWS resources, that you will be billed for if they exceed your free tier__

An example of creating a stack is shown below

`cfn-create-stack basic-test-1 --template-file basic.template`

`arn:aws:cloudformation:us-west-2:740810067088:stack/basic-test-1/bae25430-4037-11e2-ac91-50698256405b`

You can check the progress of the stack creation with the _cfn-describe-stack-events_, which you give the _stackname_.

An example of a stack creation in progress

`cfn-describe-stack-events basic-test-1`

`STACK_EVENT  basic-test-1  Ec2Instance   AWS::EC2::Instance          2012-12-07T06:35:42Z  CREATE_IN_PROGRESS`

`STACK_EVENT  basic-test-1  basic-test-1  AWS::CloudFormation::Stack  2012-12-07T06:35:37Z  CREATE_IN_PROGRESS  User Initiated`

An example of the stack creation finished

`cfn-describe-stack-events basic-test-1`

`STACK_EVENT  basic-test-1  basic-test-1  AWS::CloudFormation::Stack  2012-12-07T06:36:24Z  CREATE_COMPLETE`

`STACK_EVENT  basic-test-1  Ec2Instance   AWS::EC2::Instance          2012-12-07T06:36:24Z  CREATE_COMPLETE`    

`STACK_EVENT  basic-test-1  Ec2Instance   AWS::EC2::Instance          2012-12-07T06:35:42Z  CREATE_IN_PROGRESS`  

`STACK_EVENT  basic-test-1  basic-test-1  AWS::CloudFormation::Stack  2012-12-07T06:35:37Z  CREATE_IN_PROGRESS  User Initiated`

To delete the stack, you use the _cfn_delete_stack_ command and give it the _stackname_. An example run is shown below.

`cfn-delete-stack basic-test-1`

`Warning: Deleting a stack will lead to deallocation of all of the stack's resources. Are you sure you want to delete this stack? [Ny]y`

At this point we've covered writing some basic templates and how to get started using a template with the CLI tools.

Where to go from here
---------------------

To start you should read the [Learn Template Basics](http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/gettingstarted.templatebasics.html) and [Working with Templates](http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/template-guide.html) documentation.

While writing and exploring templates, I highly recommend getting familiar with the [Template Reference](http://docs.amazonwebservices.com/AWSCloudFormation/latest/UserGuide/template-reference.html) which has detailed docs on the various Template types, their properties, return values, etc.

Finally, Amazon has provided a wide variety of templates in the [Sample Templates library](http://aws.amazon.com/cloudformation/aws-cloudformation-templates/), ranging from [single EC2 instances](https://s3.amazonaws.com/cloudformation-templates-us-east-1/EC2InstanceSample.template), to [Drupal](https://s3.amazonaws.com/cloudformation-templates-us-east-1/Drupal_Single_Instance_With_RDS.template) or [Redmine](https://s3.amazonaws.com/cloudformation-templates-us-east-1/Redmine_Single_Instance_With_RDS.template) application stacks, and even a full blown [multi-tier application in a VPC](https://s3.amazonaws.com/cloudformation-templates-us-east-1/multi-tier-web-app-in-vpc.template), which you're able to download and run.

I've put the samples from this article in the [Github repository](https://github.com/solarce/awsadvent2012) as well.

I hope you've found this post helpful in getting started with CloudFormation.
