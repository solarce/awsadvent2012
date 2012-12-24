Exploring aws-cli
-----------------

Yesterday [Mitch Garnaat](https://twitter.com/garnaat), a Senior Engineer at Amazon, [announced](https://twitter.com/garnaat/status/282236432028930048) the _developer candidate_ release of a new AWS cli tool, _awscli_. 

The tool is open source, available under the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) license, written in [Python](http://python.org/), and the code is up on [Github](https://github.com/aws/aws-cli).

The goal of this new cli tool is to provide a __unified command line interface__ to Amazon Web Services.

It currently supports the following AWS services:

* Amazon Elastic Compute Cloud (Amazon EC2)
* Elastic Load Balancing
* Auto Scaling
* AWS CloudFormation
* AWS Elastic Beanstalk
* Amazon Simple Notification Service (Amazon SNS)
* Amazon Simple Queue Service (Amazon SQS)
* Amazon Relational Database Service (Amazon RDS)
* AWS Identity and Access Management (IAM)
* AWS Security Token Service (STS)
* Amazon CloudWatch
* Amazon Simple Email Service (Amazon SES)

This tool is still new, but it looks very promising. Let's explore some of the ways we can use it.

Getting Started
---------------

To get started with _awscli_ you'll install it, create a configuration file, and optionally add some [bash shell](http://www.gnu.org/software/bash/manual/bashref.html) completions.

__Installation__

_awscli_ can be quickly installed with either `easy_install` or `pip`

Once it is installed it you should have a _aws_ tool 
available to use. You can confirm this with the command shown below:

<pre>
$ which aws
/usr/local/bin/aws
</pre>

If you run it without any arguments if should look like this:

<pre>
$ aws
usage: aws [--output output_format] [--region region_name]
[--debug] [--profile profile_name] 
[--endpoint-url endpoint_url] [--version]
service_name

aws: error: too few arguments
</pre>

__Configuration__

You'll need to make a configuration file for it. I am assuming you've already created and know your AWS access keys.

I created my configuration file as `~/.aws`, and when you create yours, it should look like

<pre>

[default]
aws_access_key_id=<default access key>
aws_secret_access_key=<default secret key>
region=us-west-1  # optional, to define default region for this profile

</pre>

You'll want to set the _region_ to the region you have AWS resources running in.

Once you've created it, you'll set an [environement variable](http://www.cyberciti.biz/faq/set-environment-variable-linux/) to tell the _aws_ tool where to find your configuration, you can do this with the following command

<pre>
export AWS_CONFIG_FILE=/path/to/config_file
</pre>

__bash Completions__

If you're a bash shell user, you can install some handy tab completions with the following command

<pre>
complete -C aws_completer aws
</pre>

[zsh shell]() users should look at [https://github.com/aws/aws-cli/issues/5](https://github.com/aws/aws-cli/issues/5) for how to try to get completion working. 

While I am a zsh user, I am still on __4.3.11__ so I used bash for the purposes of testing out the _awscli_.


Let's test it out, the following command should return a bunch of [JSON]() output describing any instances in the region you've put in your configuration file. You can also tell _aws_ to return __text__ output by using the _--output text_ argument at the end of your command.

<pre>
aws ec2 describe-instances
</pre>

Since all the sample output is very instance specific, I don't have a good example of the output to share, but if the command works, you'll know you got the right output. __;)__

Now that we have the _aws_ tool installed and we know it's working, let's take a look at some of the ways we can use it for fun and profit.

Managing EC2
------------

The primary way a lot of you may use the _aws_ tool is to manage [EC2](http://aws.amazon.com/ec2/) instances. 

To do that with the aws command, you use the _ec2_ service name.

With the tab completion installed, you can quickly see that `aws ec2 <tab><tab>` has 144 possible functions to run.

To view your EC2 resources you use the _describe-_ commands, such as _describe-instances_ which lists all your instances, _describe-snapshots_ which lists all your EBS snapshots, or _describe-instance-status_ which you give the argument _--instance-id_ to see a specific instance.

To create new resources you use the _create-_ commands, such as _create-snapshot_ to create a new snapshot of an EBS volume or _create-vpc_ to create a new VPC.

To launch a new EC2 instance you use the _run-instances_ command, which you give a number of arguments including _--instance-type_, _--key-name_ (your ssh keypair), or _--user-data_. `aws ec2 run-instances --<tab><tab>` is a quick way to review the available options. 

There are a number of other kinds of commands available, including _attach-_, _delete-_, and _modify_. You can use the bash completion or the documentation to learn and explore all the available commands and each command's arguments.

Managing S3
-----------

Unfortunately the aws tool does not support [S3](http://aws.amazon.com/s3/) yet, but [boto](https://github.com/boto/boto) has great [S3 support](http://boto.s3.amazonaws.com/s3_tut.html), [s3cmd](http://s3tools.org/s3cmd) is popular, or you can use the [AWS S3 Console](http://docs.aws.amazon.com/AmazonS3/latest/UG/Welcome.html).

Managing CloudFormation
-----------------------

The aws tool supports managing [CloudFormation](http://aws.amazon.com/cloudformation/).

You can see your existing stacks with _list-stacks_ or see an a specific stack's resources with _list-stacks-resources_ and the _--stack-name_ argument.

You can create or delete a stack with the aptly named _create-stack_ and _delete-stack_ commands.

You can even use the handy _estimate-template-cost_ command to get a template sent through the [AWS calculator](http://calculator.s3.amazonaws.com/calc5.html) and you'll get back a URL with all your potential resources filled out.

Managing ELB
------------

The aws tool supports managing [Elastic Load Balancer (ELB)](http://aws.amazon.com/elasticloadbalancing/).

You can see your existing load balancers with the _describe-load-balancers_ command. You can create a new load balancer with the _create-load-balancer_, which takes a number of arguments, including _--availability-zones_, _--listeners_, _--subnets_ or _--security-groups_. You can delete an existing load balancer with the _delete-load-balancer_ command.

You can add or remove listeners to an existing load balancer with the _create-load-balancer-listeners_ and _delete-load-balancer-listeners_.

Managing CloudWatch
-------------------

The aws tool supports managing [CloudWatch](http://aws.amazon.com/cloudwatch/).

You can review your existing metrics with the _list-metrics_ command and your existing alarms with the _describe-alarms_ command. You can look at the alarms for a specific metric by using _describe-alarms-for-metric_ and the _--metric-name_ argument.

You can enable and disable alarm actions with the _enable-alarm-actions_ and _disable-alarm-actions_ commands. 

Where to go from here?
----------------------

You should make sure you've read the [README](https://github.com/aws/aws-cli/blob/develop/README.md).

To get more familiar with the commands and arguments, you should use both the bash completions and the built-in help.

To see the help for a specific command you invoke it like shown below:

<pre>
aws $service help
</pre>

An example is 

<pre>
$ aws ses help

NAME
    email

DESCRIPTION Amazon Simple Email Service
    This is the API Reference for Amazon Simple Email Service (Amazon SES). This
    documentation is intended to be used in conjunction with the Amazon SES Getting
    Started Guide and the Amazon SES Developer Guide.

    For specific details on how to construct a service request, please consult the
    Amazon SES Developer Guide. The endpoint for Amazon SES is located at:
    https://email.us-east-1.amazonaws.com

    delete-identity
        Deletes the specified identity (email address or domain) from the list of
        verified identities.

    delete-verified-email-address
        Deletes the specified email address from the list of verified addresses.
        The DeleteVerifiedEmailAddress action is deprecated as of the May 15, 2012
        release of Domain Verification. The DeleteIdentity action is now preferred.
--snip--
</pre>

You'll get some details on each of the available commands for a given service.

From there, if you encounter issues or had ideas for feedback you should [file an issue](https://github.com/aws/aws-cli/issues/new) on Github.

While not an official channel, I idle in __##aws__ on _irc.freenode.net_ and am happy to answer questions/provide help when I have time.





