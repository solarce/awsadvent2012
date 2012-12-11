AWS Backup Strategies
---------------------

Inspired by today's [SysAdvent](http://www.twitter.com/sysadvent) post on [Backups for Startups](http://sysadvent.blogspot.com/2012/12/day-9-backups-for-startups.html), I wanted to discuss some backup strategies for various AWS services.

As the _Backups for Startups_ post describes

> a backup is an off-line point-in-time snapshot - nothing more and nothing less. A backup is not created for fault tolerance. It is created for disaster recovery.

There are three common backup methods for achieving these point in time snapshots

* __Incremental__
* __Differential__
* __Full__

The post explains each as well as I could, some I'm just going to share with you how [Joseph Kern](http://twitter.com/josephkern) describes them

> Incremental backups are all data that has changed since the last incremental or full backup. This has benefits of smaller backup sizes, but you must have every incremental backup created since the last full. Think of this like a chain, if one link is broken, you will probably not have a working backup.

> Differential backups are all data that has changed since the last full backup. This still benefits by being smaller than a full, while removing the dependency chain needed for pure incremental backups. You will still need the last full backup to completely restore your data.

> Full backups are all of your data. This benefits from being a single source restore for your data. These are often quite large.

> A traditional scheme uses daily incremental backups with weekly full backups. Holding the fulls for two weeks. In this way your longest restore chain is six media (one weekly full, six daily incremental), while your shortest restore chain is only one media (one weekly full).

> Another similar method uses daily differentials with weekly fulls. Your longest chain is just 2 media (one differential, and one full), While your shortest is still just a single full backup.

The [article](http://sysadvent.blogspot.com/2012/12/day-9-backups-for-startups.html) also has some good suggestions on capacity planning and cost estimation, which I suggest you review before implementing the AWS backup strategies we'll learn in this post.

Let's explore, at a high level, how we can apply these backup methods to some of the most commonly used AWS services. A future post will provide some hands-on examples of using specific tools and code to do some of these kinds of backups.

Backing up Data with S3 and Glacier
-----------------------------------

[Amazon S3](http://aws.amazon.com/s3/) has been a staple of backups for many organizations for years. Often people are using S3 even when they don't use any other AWS services, because S3 provides a simple and cost effective solution to redundantly store your data off-site. A couple months ago Amazon introduced their [Glacier service](http://aws.amazon.com/glacier/), which provides archival storage to tape drives for very low cost, but at the _expense_ of having slow (multi-hour) retrieval times. Amazon recently [integrated S3 and Glacier](http://aws.typepad.com/aws/2012/11/archive-s3-to-glacier.html) to provide the best of both worlds through one API interface.

S3 is composed of two things, _buckets_ and _objects_. A bucket is a container for objects stored in Amazon S3. Every object is contained in a bucket and each object is available via a unique HTTP url. You're able to manage access to your buckets and objects through a variety of tools, including [IAM Policies](http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingIAMPolicies.html), [Bucket Policies](http://docs.amazonwebservices.com/AmazonS3/latest/dev/UsingBucketPolicies.html), and [ACLs](http://docs.amazonwebservices.com/AmazonS3/latest/dev/ACLOverview.html).

As described above, you're going to want your backup strategy to include full backups, at least weekly, and either incremental or differential backups on at least a daily basis. This will provide you with a number of point-in-time recovery options in the event of a disaster.

__Getting data into S3__

There are a number of options for getting data into S3 for backup purposes. If you want to roll your own scripts, you can use one of the many [AWS libraries](http://aws.amazon.com/code/) to develop code for storing your data in S3, performing full, incremental, and differential backups, and handling purging data older than the retention period you want to use, e.g. older than 30, 60, 90 days. 

If you're using a Unix-like operating systems, tools like [s3cmd](http://s3tools.org/s3cmd), [duplicity](http://duplicity.nongnu.org/) ([using it with S3](http://thomassileo.com/blog/2012/07/19/ubuntu-slash-debian-encrypted-incremental-backups-with-duplicity-on-amazon-s3/)), or [Amanda Backup](http://wiki.zmanda.com/index.php/Main_Page) ([using it with S3](http://wiki.zmanda.com/index.php/How_To:Backup_to_Amazon_S3)) provide a variety of options for using S3 as your backup storage, and these tools take care of a lot of the heavy lifting around doing the full, incremental, differential dance, as well as handling purging data beyond your retention period. Each tool has pros and cons in terms of implementation details and complexity vs ease of use.

If you're using Windows, tools like [Cloudberry S3 Backup Server Edition](http://www.cloudberrylab.com/windows-server-online-backup-to-amazon-s3-microsoft-azure-google-storage.aspx) (a commercial tool), [S3Sync](http://blog.jitbit.com/2012/03/automating-amazon-s3-backups-for-your.html) (a free tool), or [S3.exe](http://s3.codeplex.com/) (an open source cli tool) provide a variety of options for using S3 as your backup storage, and these tools take care of a lot of the heavy lifting around doing the full, incremental, differential dance, as well as handling purging data beyond your retention period. Each tool has pros and cons in terms of implementation details and complexity vs ease of use.


__Managing the amount of data in S3__

To implement a cost effective backup strategy with S3, I recommend that you take advantage of the Glacier integration when creating the [lifecycle policies](http://docs.amazonwebservices.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html) for each of your buckets. This effectively automates the moving of older data into Glacier and handles the purging off data beyond your retention period automatically.

Backing up EC2 instance data
----------------------------

When considering how to backup your EC2 instance data, there are a number of considerations, including the amount of data that needs to be backed up. Ideally things like your application source code, service configurations (e.g. Apache, Postfix, MySQL), and your configuration management code will all be stored in a version control system, such as Git (and on Github or Bitbucket), so that these are already backed up. But this can leave a lot of application data on file systems and in database that still needs to be backed up.

For this I'd suggest a two pronged approach, using EBS and S3. Since EBS has built-in support for [Snapshots](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/ebs-creating-snapshot.html), I suggest using EBS volumes as a place to store a near real time copy of your application data and properly quiesced dumps of your database data. And using the snapshotting to provide a sensible number of recovery points for being able to quickly restore data. Getting the data from ephemeral disks or your primary EBS volumes can easily be done with some scripting and tools like _rsync_ or _robocopy_. 

Secondly, using one of the previously discussed tools, you should be doing more long term archives from the secondary EBS volumes to S3, and optionally you can use lifecycle policies on your S3 buckets to move data into Glacier for your _longest term_ archives.

This approach involves some cost and complexity, but will provide you with multiple copies of your data and multiple options for recovery with different speed trade-offs. Specific implementation details are left as an exercise for the reader and some pragmatic examples will be part of a future post.

Backing up RDS data and configs
-------------------------------

RDS provides built-in backup and snapshotting features to help protect your data. As discussed in the [RDS post](http://awsadvent.tumblr.com/post/37091111493/amazon-relational-database-service), I recommend you deploy RDS instances in a [multi-AZ scenario](http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/RDSFAQ.MultiAZ.html) whenever possible, as this reduces the uptime impact of performing backups.

RDS has a built in [automated backups](http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html) feature that will automatically perform daily backups at a scheduled time, with the caveat that it will cause an I/O pause of your RDS instance during the snapshot, for up to 35 days. These backups are stored on S3 storage for additional protection against data-loss.

RDS also supports making [user initiated snapshots](http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html) at any point in time, with the caveat that it will cause an I/O pause of your RDS instance during the snapshot, which can be mitigated with multi-AZ deployments. These snapshots are stored on S3 storage for additional protection against data-loss.

Additionally, because of how RDS instances do transaction logging, you're able to do point-in-time restores to [any point within the automated backup recovery window](http://docs.amazonwebservices.com/AmazonRDS/latest/UserGuide/USER_PIT.html).

The only potential downside to these backup and snapshot features is that they're isolated to the region your RDS instances run in. To provide DR copies of your database data to another region you'll need to create a solution for this. One approach that is relatively low cost is to run a t1.micro in another region with a scheduled job that connects to your main RDS instance, performs a native SQL backup to local storage, then uploads the native SQL backup to S3 storage in your _DR region_. This kind of solution can have performance and cost considerations for large amounts of database data and so must be considered carefully before implementing.

Backing up AWS service configurations
-------------------------------------

While Amazon has built their services to be highly available and protect your data, it's always important to ensure you have your own backups of any critical data. 

Services like [Route53](aws.amazon.com/route53/) or [Elastic Load Balancing (ELB)](http://aws.amazon.com/elasticloadbalancing/) don't store application data, but they do store data critical to rebuilding your application infrastructure in the event of a major failure, or if you're trying to do disaster recovery in another region.

Since these services are all accessible through HTTP APIs, there are opportunities to roll your own backups of your AWS configuration data.

__Route 53__

With Route 53, you could get a [list of your Hosted Zones](http://docs.amazonwebservices.com/Route53/latest/APIReference/API_ListHostedZones.html), then get the [details of each Zone](http://docs.amazonwebservices.com/Route53/latest/APIReference/API_GetHostedZone.html). Finally, you could get the [details of each DNS record](http://docs.amazonwebservices.com/Route53/latest/APIReference/API_ListResourceRecordSets.html). Once you have all this data, you can save it into a text format of your choice and upload it to S3 in another region. A [ruby implementation](https://github.com/Hack56/Route53-To-S3) of this idea is already available.

__ELB__

With ELB, you could get a [list of all your Load Balancer instances](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/APIReference/API_DescribeLoadBalancers.html), then store the data in a text format of your choice and finally upload it to S3 in another region. I did not find any existing implementations of this with some quick searching, but one could quickly be built using the [AWS library](http://aws.amazon.com/code/) of your choosing.

Summary
-------

In summary, there are a number of great options for building a backup strategy and implementation that will meet your organizations retention, disaster recovery, and cost needs. Most of which are free and/or open source, and can be built in a highly automated fashion.

In a future post we'll get hands-on about implementing some of these ideas in an automated fashion with the [Boto](http://github.com/boto/boto) Python library for AWS.

