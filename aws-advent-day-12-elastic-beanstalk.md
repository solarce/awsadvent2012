Amazon Elastic Beanstalk
------------------------

[Elastic Beanstalk (EB)](http://aws.amazon.com/elasticbeanstalk/faqs/#what-is) is a service which helps you easily manage and deploy your application code into an automated application environment. It handles provisioning AWS resources like EC2 instances, ELB instances, and RDS databases, and let's you focus on writing your code and deploying with a `git push` style deployment when you're ready to deploy to development, staging, or production environments.

[What does Elastic Beanstalk offer me? FAQ](http://aws.amazon.com/elasticbeanstalk/faqs/#can-do)
[Getting Started Walkthrough](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/GettingStarted.Walkthrough.html)
[What Is AWS Elastic Beanstalk and Why Do I Need It?](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/Welcome.html)

Pricing
-------

AWS Elastic Beanstalk is free, but the AWS resources that AWS Elastic Beanstalk provides are live (and not running in a sandbox). You will incur the standard usage fees for any resources your environment uses, until you terminate them.

The total charges for the activity we'll do during this blog post will be minimal (typically less than a dollar). It is possible to do some testing of EB in [Free tier](http://aws.amazon.com/free/) by following [this guide](http://docs.amazonwebservices.com/gettingstarted/latest/awsgsg-freetier/deploy-sample-app.html).

[Further Reading on Pricing](http://aws.amazon.com/pricing/elasticbeanstalk/)

Key Concepts
------------

The key concepts when trying to understand and use Elastic Beanstalk are

* Application
* Environment
* Version
* Environment Configuration
* Configuration Template

The primary AWS services that Elastic Beanstalk can/will use are

* Amazon Elastic Compute Cloud (Amazon EC2)
* Amazon Relational Database Service (Amazon RDS)
* Amazon Simple Storage Service (Amazon S3)
* Amazon Simple Notification Service (Amazon SNS)
* Amazon CloudWatch
* Elastic Load Balancing
* Auto Scaling

It's important to understand what each of the main components in Elastic Beanstalk, so let's explore them in a little more depth.

__Application__

An AWS Elastic Beanstalk application is a logical collection of AWS Elastic Beanstalk components, including environments, versions, and environment configurations. In AWS Elastic Beanstalk an application is conceptually similar to a folder.

__Version__

In AWS Elastic Beanstalk, a version refers to a specific, labeled iteration of deployable code. A version points to an Amazon Simple Storage Service (Amazon S3) object that contains the deployable code (e.g., a Java WAR file). A version is part of an application. Applications can have many versions.

__Environment__

An environment is a version that is deployed onto AWS resources. Each environment runs only a single version, however you can run the same version or different versions in many environments at the same time. When you create an environment, AWS Elastic Beanstalk provisions the resources needed to run the application version you specified. For more information about the environment and the resources that are created, see Architectural Overview.

__Environment Configuration__

An environment configuration identifies a collection of parameters and settings that define how an environment and its associated resources behave. When you update an environment’s configuration settings, AWS Elastic Beanstalk automatically applies the changes to existing resources or deletes and deploys new resources (depending on the type of change).

__Configuration Template__

A configuration template is a starting point for creating unique environment configurations. Configuration templates can be created or modified only by using the AWS Elastic Beanstalk command line utilities or APIs.

__Further Reading__

* [Architectural Overview](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/concepts.concepts.architecture.html)
* [Design Considerations](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/concepts.concepts.design.html)
* [Architecting for the Cloud: Best Practices](http://media.amazonwebservices.com/AWS_Cloud_Best_Practices.pdf)

Workflow
--------

The typical workflow for using Elastic Beanstalk is that you'll create one or more _environments_ for a given _application_. Commonly development, staging, and production environments are created.

As you're ready to deploy new _versions_ of your _application_ to a given _environment_, you'll upload a new _version_ and _deploy_ it to that _environment_ via the AWS console, the CLI tools, an IDE, or the an EB API library.

* [Deploying PHP using the CLI and Git](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP_eb.sdlc.html)
* [Deploy .NET Using AWS Toolkit for Visual Studio](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_NET.html)
* [Deploy Java Using AWS Toolkit for Eclipse](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Java.html)

Supported Languages
-------------------

Elastic Beanstalk currently supports the following languages:

* [Java](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Java.sdlc.html)
* [.NET](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_NET.quickstart.html)
* [PHP](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP_eb.sdlc.html)
* [Python](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html)
* [Ruby](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Ruby_rails.html)

Getting Started
---------------

To get started with Elastic Beanstalk, we'll be using the [AWS console](https://console.aws.amazon.com/elasticbeanstalk/).

1. Login to the console and choose the Elastic Beanstalk service. 
2. Select your application platform, we'll use Python for this example, then click Start
3. AWS will begin provisioning you a new application environment. This can take a few minutes since it involves provisioning at least one new EC2 instance. EB is performing a number of steps while you wait, including
 * Creating an AWS Elastic Beanstalk application named "My First Elastic Beanstalk Application."
 * Creating a new application version labeled "Initial Version" that refers to a default sample application file.
 * Launching an environment named "Default-Environment" that provisions the AWS resources to host the application.
 * Deploying the "Initial Version" application into the newly created "Default-Environment."
4. Once the provisioning is finished you are able to view the default application by expanding the Environment Details and clicking on the URL

At this point we have a deployed EB managed application environment.

[Further Reading](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/GettingStarted.html)

Deploying an application
------------------------

There are two ways to deploy applications to your EB environments

1. Manually through the [AWS console](https://console.aws.amazon.com/elasticbeanstalk/)
2. Using the [AWS DevTools](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP.html), in conjunction with [Git](http://git-scm.com/) or an IDE like Visual Studio or Eclipse.

__Manual Deploy__

Let's do a manual update of the application through the console

1. Since we're using Python as our example framework, I am using the [python sample](https://s3.amazonaws.com/elasticbeanstalk-samples-us-east-1/python-secondsample.zip) from the [Getting Started](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/GettingStarted.Walkthrough.html) walk through
2. Login to the [EB console](https://console.aws.amazon.com/elasticbeanstalk/)
3. Click on the Versions tab
4. Click Upload New Version
5. Enter Second Version for the Version Label
6. Choose the python-secondsample.zip and Upload it
7. Under Deployment choose Upload, leave the environment set to Default-Environment
8. Click Upload New Version
9. You should now see Second Version available on the Versions tab

Now we can deploy the new version of the application to our environment

1. Check the box next to Second Version
2. Click the Deploy button
3. Set Deploy to: to Default-Environment
4. Click Deploy Version
5. Below your list of Versions it will now display the Default-Environment.
6. You can click on the Events tab to watch the progress of this deploy action.
7. Wait for the _Environment update completed successfully._ event to be logged.

Once the deployment is finished, you can check it by 

1. Clicking on the Overview tab
2. Expanding your application environment, e.g. Default-Environment
3. Reviewing the __Running Version__ field. 
4. It should now say __Second Version__

__CLI Deploy__

Being able to deploy from the command line and with revision control is ideal. So Amazon has written a set of tools, the [AWS DevTools](http://aws.amazon.com/code/6752709412171743), that integrate with Git to help get this workflow up and running.

Let's walk through doing a CLI deploy. I am going to assume you already have Git installed.

1. Get the [ELB command line tools](http://aws.amazon.com/code/6752709412171743) downloaded and [installed](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/usingCLI.html)
2. Unzip the [python sample](https://s3.amazonaws.com/elasticbeanstalk-samples-us-east-1/python-secondsample.zip) into a directory and initialize that directory as a Git repository with `git init`
3. Adding everything in the directory to the repo with `git add *` and commit it with `git commit -a -m "all the things"`
4. From your Git repository directory, run _AWSDevTools-RepositorySetup.sh_. You can find AWSDevTools-RepositorySetup.sh in the _AWS DevTools/Linux_ directory. You need to run this script for each Git repository.
5. Follow the [Git setup steps](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP.sdlc.html#create_deploy_PHP.sdlc.deploy) to setup the DevTools with your AWS credentials, application, and environment names.
6. Edit _application.py_ in your Git repo and add a comment like `# I was here`
7. Commit this change with `git commit -a -m "I was here"`
8. Push your change to your EB application environment with `git aws.push`, you can see what this should look like in the example on [deploying a PHP app with Git and DevTools](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP.sdlc.html#create_deploy_PHP.sdlc.deploy)
9. If you're Push succeeds, you should see the Running Version of your application show the [Git SHA1](http://git-scm.com/book/en/Git-Internals-Git-Objects) of your commit.

You can now continue to work and deploy by committing to Git and using `git aws.push`

__Further Reading__

* [Deploying Versions to Existing Environments](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html)
* [Deploying Versions with Zero Downtime](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.CNAMESwap.html)
* [Working with Logs](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html)

Application Environment Configurations
--------------------------------------

Once you're familiar and comfortable with deploying applications, you'll likely want to customize your application environments. Since EB uses EC2 instances running Linux or Windows, you have a certain amount of flexibility in what customizations you can make to the environment.

__Customizing Instance Options__

You're able to tweak many options regarding your instances, ELB, Auto-Scaling, and Database options, including

* Instance type
* EC2 security group
* Key pairs
* Port and HTTPS options for ELB
* Auto-Scaling instance settings and AZ preference
* Setting up your environment to use RDS resources.

To customize these things, you

1. Login to the AWS console
2. Locate your environment and click on Actions
3. Make your desired changes to the settings
4. Click Apply Changes

As mentioned, some changes can be done on the fly, like ELB changes, while others, like changing the instance size or migrating to RDS, require a longer period of time and some application downtime.

[Further reading on Environment Customization](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.managing.html)


__Customizing Application Containers__

At this time, the following container types support customization

* Tomcat 6 and 7 (non-legacy container types)
* Python
* Ruby 1.8.7 and 1.9.3
* Currently, AWS Elastic Beanstalk does not support configuration files for PHP, .NET, and legacy Tomcat 6 and 7 containers.

You're able to customize a number of things, including

* Packages
* Sources
* Files
* Users
* Groups
* Commands
* Container_commands
* Services
* Option_settings

[Further Readingon Application Container Customization](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/customize-containers.html)

Where to go from here
---------------------

Now that you're used Elastic Beanstalk, seen how to deploy code, learned how to customized your instances, you may be considering running your own application with Elastic Beanstalk.

Some of the things you'll want to look into further if you want to deploy your application to EB are:

* [Configuring HTTPS](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/configuring-https.html)
* [Using your own DNS names (Custom DNS)](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/customdomains.html)
* [Using CloudFront with EB](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudfront.html)
* [Using ElasticCache with EB](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/AWSHowTo.ElastiCache.html)
* [Using VPC with EB](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/AWSHowTo-vpc-requirements.html)
* [How can I use IAM with EB](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/AWSHowTo.iam.html)