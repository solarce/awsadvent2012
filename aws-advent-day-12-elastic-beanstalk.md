Amazon Elastic Beanstalk
------------------------

[Elastic Beanstalk (EB)]() is ...

[Further Reading]()

Pricing
-------

AWS Elastic Beanstalk is free, but the AWS resources that AWS Elastic Beanstalk provides are live (and not running in a sandbox). You will incur the standard usage fees for any resources your environment uses, until you terminate them.

The total charges for the activity we'll do during this blog post will be minimal (typically less than a dollar). It is possible to do some testing of EB in [Free tier](http://aws.amazon.com/free/) by following [this guide](http://docs.amazonwebservices.com/gettingstarted/latest/awsgsg-freetier/deploy-sample-app.html).

[Further Reading on Pricing](http://aws.amazon.com/pricing/elasticbeanstalk/)

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

[Further Reading]()

Deploying an application
------------------------

There are two ways to deploy applications to your EB environments

1. Manually through the [AWS console]()
2. Using the [AWS DevTools](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_PHP.html), in conjunction with [Git](http://git-scm.com/) or an IDE like Visual Studio or Eclipse.

__Manual Deploy__

Let's do a manual update of the application through the console

1. Since we're using Python as our example framework, I am using the [python sample](https://s3.amazonaws.com/elasticbeanstalk-samples-us-east-1/python-secondsample.zip) from the [Getting Started](http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/GettingStarted.Walkthrough.html) walk through
2. Login to the [EB console]([AWS console](https://console.aws.amazon.com/elasticbeanstalk/)
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

Scaling an application
----------------------

[Further Reading]()

Where to go from here
---------------------

[Further Reading]()