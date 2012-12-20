Automating Backups in AWS
-------------------------

In [Day 9's post](http://awsadvent.tumblr.com/post/37590181796/aws-backup-strategies) we learned about some ideas for how to do proper backups when using AWS services.

In today's post we'll take a hands-on approach to automating creating resources and performing the action needs to achieve these kinds of backups, using some [bash](http://tldp.org/LDP/abs/html/) scripts and the [Boto](https://github.com/boto/boto) python library for AWS. 

Ephemeral Storage to EBS volumes with rsync
-------------------------------------------

Since IO performance is key for many applications and services, it is common to use your EC2 instance's [ephermeral storage](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html) and [Linux software raid](http://linux.die.net/man/4/md) for your instance's local data storage. While [EBS](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html) volumes can have erratic performance, they are useful to provide backup storage that's not tied to your instance, but is still accessible through a filesystem.

The approach we're going to take is as follows:

1. Make a two EBS volume software raid1 and mount as /backups
2. Make a shell script to rsync /data to /backups
3. Set the shell script up to run as a cron job

__Making the EBS volumes__

Adding the EBS volumes to your instance can be done with a simple Boto script

_add-volumes.py_

<pre>

</pre>

Once you've run this script you'll have two new volumes attached as local devices on your EC2 instance.

__Making the RAID1__

Now you'll want to make a two volume RAID1 from the EBS volumes and make a filesystem on it.

The following shell script takes care of this for you

_make-raid1-format.sh_

<pre>

</pre>

Now you have a _/backups/_ you can rsync files and folders to for your backup process.

__rsync shell script__

[rsync](http://rsync.samba.org/) is the best method for syncing data on Linux servers.

The following shell script will use rsync to make backups for you.

_rsync-backups.sh_

<pre>

</pre>


__making a cron job__

To make this a cron job that runs once a day, you can add a file like the following, which assumes you put rsync-backups.sh in /usr/local/bin

This cron job will run as root, at 12:15AM in the timezone of the instance.

_/etc/cron.d/backups_

<pre>
MAILTO="me@me.biz"
15 00 * * * root /usr/bin/flock -w 10 /var/lock/backups /usr/local/bin/rsync-backups.sh > /dev/null 2>&1

</pre>

__Data Rotation, Retention, Etc__

To improve on how your data is rotated and retained you can explore a number of open source tools, including:

* [rsnapshot](http://www.rsnapshot.org/)
* [duplicity](http://duplicity.nongnu.org/)
* [rdiff](http://rdiff-backup.nongnu.org/)

EBS Volumes to S3 with boto-rsync
-------------------------------

Now that you've got your data backed up to EBS volumes, or you're using EBS volumes as your main source of datastore, you're going to want to ensure a copy of your data exists elsewhere. This is where S3 is a great fit.

As you've seen, _rsync_ is often the key tool in moving data around on and between Linux filesystems, so it makes sense that we'd use an _rsync_ style utility that talks to S3.

For this we'll look at how we can use [boto-rsync](https://github.com/seedifferently/boto_rsync).

> boto-rsync is a rough adaptation of boto's s3put script which has been reengineered to more closely mimic rsync. Its goal is to provide a familiar rsync-like wrapper for boto's S3 and Google Storage interfaces.

> By default, the script works recursively and differences between files are checked by comparing file sizes (e.g. rsync's --recursive and --size-only options). If the file exists on the destination but its size differs from the source, then it will be overwritten (unless the -w option is used).

_boto-rsync_ is simple to use, being as easy as `boto-rsync [OPTIONS] /local/path/ s3://bucketname/remote/path/`, which assumes you have your AWS key put in `~/.boto` or the ENV variables set.

_boto-rsync_ has a number of options you'll be familiar with from _rsync_ and you should consult the [README](https://github.com/seedifferently/boto_rsync/blob/master/README.rst) to get more familiar with this.

As you can see, you can easily couple _boto-rsync_ with a cron job and some script to get backups going to S3.

Lifecycle policies for S3 to Glacier
------------------------------------

One of the recent features added to S3 was the ability to use [lifecycle policies](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html) to archive your [S3 objects to Glacier](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-archival.html)

You can create a lifecycle policy to archive data in an S3 bucket to glacier very easily with the following boto code.

_s3-glacier.py_

<pre>

</pre>

Conclusion
----------

As you can see, there are many options for automating your backups on AWS in comprehensive and flexible ways, and this post is only the tip of the _iceberg_.