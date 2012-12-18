Using IAM to Increase Flexibility and Security
----------------------------------------------

Today's post is a contribution from [Erik Hollensbe](http://erik.hollensbe.org/), an active member of the [Chef](http://www.opscode.com/chef) and Operations communities online and a practicing Operations Engineer.


[AWS IAM (Identity and Access Management)](http://docs.aws.amazon.com/IAM/latest/UserGuide/Welcome.html) is a tool to apply ACLs to AWS
credentials -- it's not much more than that.  While this sounds pretty banal, it can be used to solve a number of problems with both the flexibility and security of your network.

Scare Tactics Time
------------------

A lot of companies and groups use AWS exclusively, where previously they would
have used racks of machines in a data center. Short of having a working
proximity card and a large bucket of water, there wasn't much you were going to
be able to do to cause irreparable damage to every component of your company's
network.  Presuming you did that, and didn't kill yourself by electrocution,
you still have to evade the DC cameras to get away with it.

That all changes with something like AWS. The master keys to your account can
literally be used to destroy everything. Your machines, your disks, your
backups, your assets. Everything. While vendor partitioning, off site backups,
etc, is an excellent strategy (aside from other, separate gains) to mitigate
the long-term damage, it doesn't change this.  Plus since the credentials are
shared, it's not exactly a feat to do this anonymously.

While my intent isn't to scare you into using IAM, it's important to understand
that in more than a few organizations, not only will many members of your staff
have these credentials, but frequently enough they will also live on the
servers as part of code deploys, configuration management systems, or one-off
scripts. So you don't even have to work at the company in that situation, you
simply need to find a hole to poke open to tear down an entire network.

Security Theatre in a Nutshell
------------------------------

Before I go into how to use IAM to solve these problems, I'm going to balance
this out with a little note about security theatre.

Know the problem you're actually solving. If you're not clear on what you're
solving, or it's not a full solution, you're practicing the worst kind of
security theatre, wasting everyone's time as a result. Good security is as much
about recognizing and accepting risk as mitigating it. Some of these solutions
may not apply to you and some of them may not be enough. Use your head.

IAM as a tool to mitigate turnover problems
-------------------------------------------

This is the obvious one, so I'll mention it first. Managing turnover is
something that's familiar to anyone with significant ops experience, whether or
not they had any hand in the turnover itself. Machines and networks are
expected to be protected from reprisals and a good ops person is thinking about
this way ahead of when it happens for the first time.

Just to be clear, no human likes discussing this subject, but it is a necessity
and an unfortunate consequence of both business and ops. Ignoring it isn't a
solution.

IAM solves these problems in a number of ways:

* Each user gets their own account to both log in to the web interface and
  associated credentials to use. 
* Users are placed in groups which have policies (ACLs). Users individually
  have policies as well and these can cascade. Policies are just JSON objects,
  so they're easy to re-use, keep in source control, etc.

Most users have limited needs and it would be wise to (without engaging in
security theatre) assess what those needs are and design policies
appropriately. Even if you don't assign restrictive policies, partitioning
access by user makes credential revocation fast and easy, which is exactly what
you want and need in an unexpected turnover situation... which is usually the
time when it actually matters.

And who watches the watchers? Let's be honest with ourselves for a second. You
may be behind the steering wheel, but you probably aren't the final word on the
route to take, and anyone who thinks they are because they hold the access keys
needs more friends in the legal profession. Besides, it's just not that
professional. Protect your network against yourself too. It's just the right
thing to do.

So, here's the shortest path to solving turnover problems with AWS credentials:

* Bootstrap IAM -- click on IAM in the AWS control panel. Set up an admin group
  (the setup will offer to create this group for you) and a custom URL for your
  users to log in to.
* Set up users for everyone who needs to do anything with AWS. Make them
  admins. (Admins still can't modify the owner settings, but they can affect
  other IAM users.)
* Tell your most senior technical staff to create a new set of owner
  credentials, to change the log in password, and to revoke the old
  credentials.

Now you're three clicks away (or an API call) from dealing with any fear of
employee reprisal short of the CTO, and you have traceable legal recourse in
case it took you too long to do that. Congratulations.

IAM as a tool to scope automated access
---------------------------------------

Turnover is not a subject I enjoy discussing when it comes to security, but
it's the easier introduction. While I think the above is important, it's
arguably the lesser concern.

As our applications and automation tooling like configuration management
becomes more involved and elaborate, we start integrating parts of the AWS API.
Whether that's a web app uploading files to a S3 bucket, a deploy script that
starts new EC2 machines, or a chef recipe that allocates new volumes from EBS
for a service to use, we become dependent on the API. This is a good thing, of
course -- the API is really where the win is in using a service like AWS.

However, those credentials have to live somewhere. On disk, in a central
configuration store, encrypted, unencrypted, it doesn't matter. If your
automation or app can access it, an attacker that wants it will get it.

Policies let us scope what credentials can do. Does your app syncing assets
with S3 and cloudfront need to allocate EBS volumes, or manage Route53 zones?
Prrrrrroobably not. If it's easier to think about this in unix terms, does
`named` need to access the contents of `/etc/shadow`?

"Well, duh!", you might say, yet many companies plug owner credentials directly
into their S3 or EBS allocation tooling, and then run on EC2 under the same
account. We preach loudly about not running as root, but then expose our entire
network (not just that machine) to plunder.

Instead, consider assigning policies to different IAM accounts that allow
exactly what that tool needs to do, and making those credentials available to
that tool. Not only will you mitigate access issues, but it will be clearer
when your tooling is trying to do something you didn't expect it to do by
side-effect, just like a service or user on your machine messing with a file
you didn't expect it to.

You can populate these credentials with your favorite configuration management
system, or credentials can also be [associated to EC2 instances directly](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/UsingIAM.html#UsingIAMrolesWithAmazonEC2Instances),
where the metadata is available from an internally-scoped HTTP request.

Creating a Policy
-----------------

An IAM policy is just a JSON-formatted file with a simple schema that looks
something like this:

```
{
  "Statement": [
    {
      "Sid": "Stmt1355374500916",
      "Action": [
        "ec2:CreateImage"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

Some highlights:

* A `Statement` is a hash describing a rule.
* `Actions` are a 1:1 mapping to AWS API calls. For example, the above
  statement references the `CreateImage` API call from the `ec2` API.
* `Effect` is just how to restrict the Action. Valid values are `Allow` and `Deny`.
* A `Resource` is an ARN, which is just a qualified namespace. In the EC2 case
  ARNs have no effect, but you'd use one if you were referring to something
  like a S3 bucket.

For extended policy documentation, [look here](http://docs.amazonwebservices.com/IAM/latest/UserGuide/AccessPolicyLanguage.html).

One of my favorite things about AWS policies is that they're JSON. This JSON
file can be saved in source control and re-used for reference, repeat purposes,
or in a DR scenario.

AWS itself provides a pretty handy [Policy Generator](http://awspolicygen.s3.amazonaws.com/policygen.html) for making this
a little easier. You will still want to become familiar with the API calls to
write effective policies, but there is also a small collection of [example policies](http://aws.amazon.com/code/AWS-Policy-Examples) while you get your
feet wet.

Happy Hacking!
