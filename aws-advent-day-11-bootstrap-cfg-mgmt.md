Bootstrapping Config Management on AWS
--------------------------------------

When using a cloud computing provider like [AWS's EC2](https://aws.amazon.com/ec2/) service, being able to ensure that all of your instances are running the same configuration and being able to know that new instances you create can be quickly configured to meet your needs is critical. 

[Configuration Management](http://en.wikipedia.org/wiki/Configuration_management#Operating_System_configuration_management) tools are the key to achieving this. In my experience so far, the two most popular open source configuration management tools are PuppetLabs' [Puppet](http://puppetlabs.com/puppet/what-is-puppet/) and Opscode's [Chef](http://www.opscode.com/chef/) products. Both are open source, written in Ruby, and you're able to run your own server and clients without needing to purchase any licensing or support. Both also have vibrant and passionate communities surrounding them. These are the two we will focus on for the purposes of this post.

Getting started with using Puppet or Chef itself and/or building the Puppet or Chef server will not be the focus of this post, but I will provide some good jumping off points to learn more about this. I am going to focus on specifically on some techniques for bootstrapping the Puppet and Chef clients onto Linux EC2 instances.

user-data and cloud-init
------------------------

Before getting into the specifics of bootstrapping each client, let's take a look at two important concepts/tools for Linux AMIs

__user-data__

user-data is a [piece of instance metadata](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/AESDG-chapter-instancedata.html) that is available to your EC2 instances at boot time and during the lifetime of your instance. 

At boot time for [Ubuntu AMIs](http://cloud-images.ubuntu.com/locator/ec2/) and the [Amazon Linux AMI](http://aws.amazon.com/amazon-linux-ami/), this user-data is passed to cloud-init during the first bootup of the EC2 instance, and cloud-init will read the data and can execute it.

So a common technique for bootstrapping instances is to pass the contents of a shell script to the [EC2 API](http://docs.amazonwebservices.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-RunInstances.html) as the _user-data_, the shell code is executed during boot, as the root user, and your EC2 instance is modified accordingly.

This is the technique we will use to help bootstrap our config management clients.

__cloud-init__

cloud-init is the Ubuntu package that handles early initialization of a cloud instance. It is installed in the official [Ubuntu images available on EC2](http://cloud-images.ubuntu.com/locator/ec2/) and Amazon also includes it in their [Amazon Linux AMI](http://aws.amazon.com/amazon-linux-ami/).

It provides a wide variety of built-in functions you can use to customize and configure your instances during bootup, which you send to cloud-init via user-data. It also supports the ability to run arbitrary shell commands.

It's definitely possible to use cloud-init as a lightweight way to do config management style actions at bootup, but you're left to build your own tools to make additional modifications to your EC2 instances during their lifecycle.

In our case we're going to take advantage of user-data and cloud-init to use curl to download a shell script from S3 that takes care of our client bootstrapping, as this technique translates well to any Linux distributions, not just those which include cloud-init. And this is also easily re-usable in other cloud provider environments, your own data center, or home lab/laptop/local dev environement(s).

Bootstrapping Puppet
--------------------

To bootstrap Puppet, you'll need two things

1. A Puppetmaster where you can sign the certificate the client generates
2. A shell script, _puppet-bootstrap.sh_, which installs the Puppet agent and connecting it to the puppetmaster

The process of bootstrapping works as follows

1. You provision an EC2 instance, passing it user-data with the shell script
2. The EC2 instance runs the _puppet-bootstrap.sh_ script on the instance
3. The shell script installs the Puppet client, sets the server in _puppet.conf_, and starts the Puppet service.

__puppet-bootstrap.sh__

So [Michtell Hashimoto](https://twitter.com/mitchellh) of [Vagrant](http://vagrantup.com) fame has recently started an amazing [puppet-bootstrap](https://github.com/hashicorp/puppet-bootstrap) repository on Github. So grab the script for the distribution type, RHEL,  Debian/Ubuntu, etc, and save it locally.

Then add the following two lines to the script

```
echo "server=puppetmaster.you.biz" >> /etc/puppet/puppet.conf
echo "listen=true" >> /etc/puppet/puppet.conf
```

Save the script and pass it in as your _user-data_.

__Client certificate signing__

The final step is to sign the client's certificate on your Puppetmaster.

You can do this with the following command

	puppet cert --sign ec2.instance.name

At this point you can give the instance a node definition and begin applying your classes and modules.

Bootstrapping Chef
------------------

To bootstrap Chef onto you're going to need five things

1. A [Chef server](http://wiki.opscode.com/display/chef/Chef+Server) or [Hosted Chef account](http://www.opscode.com/hosted-chef/)
2. A [client.rb](http://wiki.opscode.com/display/chef/Installing+Chef+Client+on+Ubuntu+or+Debian#InstallingChefClientonUbuntuorDebian-Configurechefclient) in an S3 bucket, with what you want your instance default settings to be
3. Your __validation.pem__ (__ORGNAME-validator.pem__ if you're using Hosted Chef), in an S3 bucket
4. A shell script, _chef-bootstrap.sh_, to install the [Omnibus installer]() and drop your files in place, which you pass in as _user-data_
5. An IAM role that includes read access to the above S3 bucket

The process of bootstrapping works as follows

1. You provision an EC2 instance, passing it the IAM role and user-data with the shell script
2. The EC2 instance runs the _chef-bootstrap.sh_ script on the instance
3. The shell script installs the Omnibus Chef client, drops the _.pem_, and _client.rb_ in place and kicks off the first chef-client run

__Creating the IAM Role__

To create the IAM role you do the following

1. Login to the [AWS console](https://console.aws.amazon.com)
2. Click on the [IAM service](https://console.aws.amazon.com/iam/home)
3. Click on Roles, set the Role Name
4. Click on Create New Role
5. Select AWS Service Roles, click Select
6. Select Policy Generator, click Select
7. In the Edit Permissions options
  * Set Effect to Allow
  * Set AWS Service to Amazon S3
  * For Actions, select ListAllMyBuckets and GetObject
  * For the ARN, use _arn:aws:s3:::BUCKETNAME_, e.g. _arn:aws:s3:::meowmix_
  * Click Add Statement
8. Click Continue
9. You'll see a JSON Policy Document, review it for correctness, then Click Continue
10. Click Create Role

__Files on S3__

There are many tools for uploading the files mentioned to S3, including the AWS console. I'll leave the choice of tool up to the user.

If you're not familiar with uploading to S3, see the [Getting Started Guide](http://docs.amazonwebservices.com/AmazonS3/latest/gsg/CreatingABucket.html).

__chef-bootstrap.sh__

The bootstrap.sh script is very simple, an example is included in the [Github repo](https://github.com/solarce/awsadvent2012) and shown below, the _.pem_ and _client.rb_ are geared towards Hosted Chef.

	#!/bin/bash

	# all commands run as root because they're run via cloud-init and passed in as user-data

	# install the omnibus client
	true && curl -L https://www.opscode.com/chef/install.sh | bash

	# make a directory for chef stuff
	mkdir /etc/chef

	# grab our private key for talking to hosted chef
	curl http://BUCKETNAME.s3.amazonaws.com/ORGNAME-validator.pem -o /etc/chef/ORGNAME-validator.pem

	# grab a minimal client.rb for getting the chef-client registered
	curl http://BUCKETNAME.s3.amazonaws.com/client.rb -o /etc/chef/client.rb

	#kick off the first chef run
	/usr/bin/chef-client

__client.rb__

The client.rb is very simple, an example is included in the [Github repo](https://github.com/solarce/awsadvent2012) and shown below, this _client.rb_ is geared towards Hosted Chef

	log_level        :info
	log_location     STDOUT
	chef_server_url  'https://api.opscode.com/organizations/ORGNAME'
	validation_key         "/etc/chef/ORGNAME-validator.pem"
	validation_client_name 'ORGNAME-validator'

At this point you'll have a new EC2 instance that's bootstrapped with the latest Omnibus Chef client and is connected to your Chef Server. You can begin applying roles, cookbooks, etc your new instance(s) with [knife](http://wiki.opscode.com/display/chef/Knife)

In conclusion
-------------

You've now seen some ideas and two practical applications of automating as much of the configuration management bootstrapping process as is easily possible with Puppet and Chef. These can be easily adapted for other distributions and tools and customized to suit your organizations needs and constraints.



