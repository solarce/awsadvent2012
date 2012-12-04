Amazon Relational Database Service
----------------------------------

Amazon's Relational Database Service (RDS) allows you to create and run [MySQL](http://docs.amazonwebservices.com/AmazonRDS/latest/GettingStartedGuide/LaunchDBInstance.MySQL.html), [Oracle](http://docs.amazonwebservices.com/AmazonRDS/latest/GettingStartedGuide/LaunchDBInstance.Oracle.html), or [SQL Server](http://docs.amazonwebservices.com/AmazonRDS/latest/GettingStartedGuide/LaunchDBInstance.SQLSvr.html) database servers without the need to manually create EC2 instances, manage the instance operating system, and install, then manage the database software itself. Amazon has also done the work of automating synchronous replication and failover so that you can run a pair of database instances in a [Multi-AZ](http://aws.amazon.com/about-aws/whats-new/2010/05/18/announcing-multi-az-deployments-for-amazon-rds/) (for MySQL and Oracle) with a couple clicks/API calls. And through CloudWatch integration, you're able to get metrics and alerting for your RDS database instances. As with all AWS services, you pay for your RDS instances [by the hour, with some options for paying ahead and saving some cost](http://aws.amazon.com/rds/pricing/), the cost of an RDS instance depends on the instance size, if you use Multi-AZ, the database type, if you use Provisioned IOPS, and any data transferred to the Internet or other AWS regions.

This post will take you through getting started with RDS, some of the specifics of each database engines, and some suggestions on using RDS in your application's infrastructure.

RDS instance options
--------------------

RDS instances come in two flavors, _On Demand_ and _Reserved_. _On Demand_ instances are paid for by the hour, based on the size of the instance, while _Reserved_ instances are paid for based on a one or three year basis.

RDS instance classes mirror those of normal EC2 instances and are described in detail on [Amazon's site](http://aws.amazon.com/rds/reserved-instances/#4).

A couple compelling features of RDS instance types are that 

1. You're able to scale your RDS instances up in memory and compute resources on the fly, and with MySQL and Oracle instances, you're also able to grow your storage size on the fly, from 100GB to 1TB of space.
2. You're able to use Provisioned IOPS to provide guaranteed performance to your database storage. You can provision from 1,000 IOPS to 10,000 IOPS with corresponding storage from 100GB to 1TB for MySQL and Oracle engines but if you are using SQL Server then the maximum IOPS you can provision is 7,000 IOPS.

RDS instances are automatically managed, including OS and database server/engine updates, which occur during your weekly scheduled maintenance window.

[Further Reading](http://aws.amazon.com/rds/faqs/#2)

Creating RDS instances
----------------------

We're going to assume you've already setup with an AWS IAM account and API key to manage your resources.

You can get started with creating RDS instances through one of three methods

1. The [AWS Console](https://console.aws.amazon.com/rds/)
2. AWS's [command line tools](http://aws.amazon.com/developertools)
3. The [RDS API](http://docs.amazonwebservices.com/AmazonRDS/latest/CommandLineReference/) or one of the API's many [libraries](http://aws.amazon.com/code/)

To create an RDS instance through the console, you do the following:

1. Select your region, then select the RDS service
2. Click on database instances
3. Select _Launch a database instance_
4. Select the database engine you need
5. Select the instance details, this may include the DB engine version
6. Select the instance class desired. If you're just experiment, a db.t1.micro is a low-cost option for this.
6. Select if you want this to be a Multi-AZ deployment
7. Choose the amount of allocated storage in GB
8. Select if you wish to use Provisioned IOPS (this costs extra)
9. Fill in your DB identifier, username, and desired password.
10. Choose your database name
11. You can modify the port your database service listens on, customize if you want to use a VPC, or choose your AZ. I would consider these advanced topics and details on some will be covered in future AWS Advent posts.
12. You can choose to disable backups (you really shouldn't) and then set the details of how many backups you want and how often they should be made.
13. At this point you are ready to launch the database instance, start using it (and paying for it).

To create a database instance with AWS's cli tools, you do the following: 

1. [Download](http://aws.amazon.com/developertools/2928) and [Install](http://docs.amazonwebservices.com/AmazonRDS/latest/CommandLineReference/StartCLI.html) the CLI tools
2. Once you have the tools installed and working, you'll use the [rds-create-db-instance](http://docs.amazonwebservices.com/AmazonRDS/latest/CommandLineReference/CLIReference-cmd-CreateDBInstance.html) tool to create your instance
3. An example usage of the command can be found below

	`rds-create-db-instance SimCoProd01 -s 10 -c db.m1.large -e mysql -u master -p Kew2401Sd`

To create a database instance using the API, you do the following:

1. Review the [API docs](http://docs.amazonwebservices.com/AmazonRDS/latest/APIReference/Welcome.html) to familiarize yourself with the API or obtain the [library](http://aws.amazon.com/code/) for the programming language of your choice and review it's documentation.
2. If you want to try creating an instance directly from the API, can do so with the [CreateDBInstance](http://docs.amazonwebservices.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html) API call.
3. An example of calling the API directly can be found below

	`curl -v https://rds.amazonaws.com/?Action=CreateDBInstance&DBInstanceIdentifier=SimCoProd01&Engine=mysql&MasterUserPassword=Password01&AllocatedStorage=10&MasterUsername=master&Version=2012-09-17&DBInstanceClass=db.m1.large&DBSubnetGroupName=dbSubnetgroup01&SignatureVersion=2&SignatureMethod=HmacSHA256&Timestamp=2011-05-23T05%3A54%3A53.578Z&AWSAccessKeyId=<AWS Access Key ID>&Signature=<Signature>`

Modifying existing instances
----------------------------

There are a number of modifications you can make to existing instances. Including:

* Changing the engine version of a specific database type, e.g. going from MySQL 5.1 to MySQL 5.5
* Converting a single instance to a Multi-AZ deployment.
* Increasing the allocated storage
* Changing your backup options
* Changing the scheduled maintenance window

All these kinds of changes can be made through the console, via the cli tools, or through the API/libraries.

[Further Reading](http://aws.amazon.com/rds/faqs/#20)

Things to consider when using RDS instances
-------------------------------------------

There are a number of things to consider when using RDS instances, both in terms of sizing your instances, and AWS actions that can affect your instances.

__Sizing__

Since RDS instances are easily re-sizable and include CloudWatch metrics, it is relatively simple to start with a smaller instance class and amount of storage, and grow as needed. If possible, I recommend doing some benchmarking with what you think would be a good starting point and verify if the class and storage you've chosen does meet your needs.

I would also recommend that you choose to start with using Provisioned IOPS and a Multi-AZ setup. While this is more expensive, you're guaranteeing a level of performance and reliability from the get-go, and will help mitigate some of the things below that can affect your RDS instances.

[Further Reading](http://aws.amazon.com/articles/2936?_encoding=UTF8&jiveRedirect=1)

__Backups__

Backup storage up to the amount of your instance's allocated storage is included at no additional cost, so you should at least leave the default of 1 day of backups, but should consider using a longer window, at least 7 days.

Per the [RDS FAQ on Backups](http://aws.amazon.com/rds/faqs/#23):

> The automated backup feature of Amazon RDS enables point-in-time recovery of your DB Instance. When automated backups are turned on for your DB Instance, Amazon RDS automatically performs a full daily snapshot of your data (during your preferred backup window) and captures transaction logs (as updates to your DB Instance are made). When you initiate a point-in-time recovery, transaction logs are applied to the most appropriate daily backup in order to restore your DB Instance to the specific time you requested. Amazon RDS retains backups of a DB Instance for a limited, user-specified period of time called the retention period, which by default is one day but can be set to up to thirty five days. You can initiate a point-in-time restore and specify any second during your retention period, up to the Latest Restorable Time. You can use the DescribeDBInstances API to return the latest restorable time for you DB Instance(s), which is typically within the last five minutes.

So have a good window of point-in-time and daily backups will ensure you have sufficient recovery options in the case of disaster or any kind of data loss.

The point in time recovery does not affect instances, but the daily snapshots do cause a pause in all IO to your RDS instance in the case of single instances, but if you're using a Multi-AZ deployment, this snapshot is done from the hidden secondary, causing the secondary to fall slightly behind your primary, but without causing IO pauses to the primary. This is an additional reason I recommend accepting the cost and using Multi-AZ as your default.

[Further Reading](http://aws.amazon.com/rds/faqs/#24)

__Snapshots__

You can initiate additional snapshots of the database at any time, via the console/CLI/API, which will cause a pause in all IO to single RDS instances and a pause to the hidden secondary of Multi-AZ instances.

All snapshots are stored to S3, and so are insulated from RDS instance failure. However, these snapshots are not accessible to other services, so if you're wanting backups for offsite DR, you'll need to orchestrate your own SQL level dumps via another method. A t1.micro EC2 instance that makes dumps and stores to S3 in another region is a relatively straightforward strategy for accomplishing this.

[Further Reading](http://aws.amazon.com/rds/faqs/#23)

__Upgrades and Maintenance Windows___

Because RDS instances are meant to be automatically managed, each RDS instance will have a weekly scheduled maintenance window. During this window the instance becomes unavailable while OS and database server/engine updates are applied. If you're using a Multi-AZ deployment, then your secondary will be updated, failed over to, then your previous primary is upgraded as the new secondary, this is another reason I recommend accepting the cost and using Multi-AZ as your default.

[Further Reading]()

MySQL
----------

__Multi-AZ__

MySQL RDS instances support a Multi-AZ deployment. A Multi-AZ deployment is comprised of a primary server which accepts reads and writes and a hidden secondary, in another AZ within the region, which synchronously replicates from the primary. You send your client traffic to a CNAME, which is automatically failed over to the secondary in the event of a primary failure.

Backups and snapshots are performed against the hidden secondary, and automatic failover to the secondary occurs during maintenance window activities.

[Further Reading](aws.amazon.com/rds/faqs/#111)

__Read Replicas__

MySQL RDS instances also support a unique feature called Read Replicas. These are additional replicas you create, within any AZ in a region, which asynchronously replicate from a source RDS instance. The primary in the case of Multi-AZ deployments.

[Further Reading](http://aws.amazon.com/rds/faqs/#87)

Oracle
----------

__Multi-AZ__

Oracle RDS instances support a Multi-AZ deployment. Similar in setup to the MySQL Multi-AZ setup, there is a primary server which accepts reads and writes and a hidden secondary, in another AZ within the region, which synchronously replicates from the primary. You send your client traffic to a CNAME, which is automatically failed over to the secondary in the event of a primary failure.

[Further Reading](http://aws.amazon.com/rds/faqs/#111)

SQL Server
----------

__Multi-AZ__

Unfortunately, SQL Server RDS instances do not have a Multi-AZ option at this time.

[Further Reading](http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/RDSFAQ.SQLServer.html)
