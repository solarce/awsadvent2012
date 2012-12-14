AWS EC2 Configuration Management with Chef
------------------------------------------

Today's post is a contribution from [Joshua Timberman](https://www.twitter.com/jtimberman), a Technical Community Manager at [Opscode](http://www.opscode.com), an avid RPGer and DM extraordinaire, a talented home-brewer, who is always Internet meme and Buzzword compliant.

He shares with us how [Chef](http://www.opscode.com/chef/) can help manage your [EC2](http://aws.amazon.com/ec2/) instances.

-----------------------

[In a previous post](http://awsadvent.tumblr.com/post/37773106407/bootstrap-cfg-mgmt-aws), we saw some examples about how to get started managing AWS EC2 instances with Puppet and Chef. In this post, we'll take a deeper look into how to manage EC2 instances with Chef. It is outside the scope of this post to go into great detail about building cookbooks. If you're looking for more information on working with cookbooks, see the following links

* [Guide to Creating A Cookbook](http://wiki.opscode.com/display/chef/Guide+to+Creating+A+Cookbook+and+Writing+A+Recipe)
* [How do I work with Cookbooks](http://wiki.opscode.com/display/chef/Cookbooks#Cookbooks-HowdoIworkwithcookbooks%3F)
* [Managing Cookbooks with Knife](http://wiki.opscode.com/display/chef/Managing+Cookbooks+With+Knife)


Prerequisites
-------------

There are a number of prequisites for performing the tasks outlined in this post, including

* Workstation Setup
* Authentication Credentials
* Installing Chef

__Workstation Setup__

We assume that all commands and work will originate from a local workstation. For example, a company-issued laptop. We'll take for granted that it is running a [supported platform](http://docs.opscode.com/install_system_requirements.html). You'll need some authentication credentials, and configure knife.

__Authentication Credentials__

You'll need the [Amazon AWS credentials](http://docs.amazonwebservices.com/AWSEC2/latest/UserGuide/SettingUp_CommandLine.html#set-aws-credentials) for your account. You'll also need to create an [SSH key pair](http://docs.amazonwebservices.com/AWSEC2/latest/CommandLineReference/ApiReference-cmd-ImportKeyPair.html) to use for your instances. Finally, if you're using a Chef Server, you'll need your [user key and the "validation" key](http://wiki.opscode.com/display/chef/Omnibus+Workstation+Setup+for+Linux+and+Mac#OmnibusWorkstationSetupforLinuxandMac-CreateaChefRepositoryonyourWorkstation)

__Install Chef__

If your local workstation system doesn't already have Chef installed,
Opscode recommends using the ["Omnibus package" installers](http://opscode.com/chef/install).

Installing the knife-ec2 Plugin
-------------------------------

Chef comes with a a plugin-based administrative command-line tool called knife. Opscode publishes the [knife-ec2](http://rubygems.org/gems/knife-ec2) plugin which extends knife with [fog](http://rubygems.org/gems/fog) to interact with the EC2 API. This plugin will be used in further examples, and it can be installed as a RubyGem into the ["Omnibus"](http://wiki.opscode.com/display/chef/Omnibus+Workstation+Setup+for+Linux+and+Mac#OmnibusWorkstationSetupforLinuxandMac-CreateaChefRepositoryonyourWorkstation) Ruby environment that comes
with Chef.

__example__

`sudo /opt/chef/embedded/bin/gem install knife-ec2`

If you're using a different Ruby environment, you'll need to use the proper gem command.

### knife.rb

In order to use knife with your AWS account, it must be configured. The example below uses Opscode Hosted Chef as the Chef Server. It includes the AWS credentials as read in from shell environment variables. This is so the actual credentials aren't stored in the config file directly.

Normally, the config file lives in `./.chef/knife.rb`, where the current directory is a "Chef Repository." See the [knife.rb documentation](http://docs.opscode.com/config_rb_knife.html) for more information.

__example__

    current_dir = File.dirname(__FILE__)
    log_level                :info
    log_location             STDOUT
    node_name                "YOUR_USERNAME"
    client_key               "#{current_dir}/YOUR_USERNAME.pem"
    validation_client_name   "YOUR_ORGNAME-validator"
    validation_key           "#{current_dir}/YOUR_ORGNAME-validator.pem"
    chef_server_url          "https://api.opscode.com/organizations/YOUR_ORGNAME"
    cache_type               'BasicFile'
    cache_options( :path => "#{ENV['HOME']}/.chef/checksums" )
    cookbook_path            ["#{current_dir}/../cookbooks"]

    knife[:aws_access_key_id]      = ENV['AWS_ACCESS_KEY_ID']
    knife[:aws_secret_access_key]  = ENV['AWS_SECRET_ACCESS_KEY']

    # Default flavor of server (m1.small, c1.medium, etc).
    #knife[:flavor] = "m1.small"

    # Default AMI identifier, e.g. ami-12345678
    #knife[:image] = ""

    # AWS Region
    #knife[:region] = "us-east-1"

    # AWS Availability Zone. Must be in the same Region.
    #knife[:availability_zone] = "us-east-1b"

    # A file with EC2 User Data to provision the instance.
    #knife[:aws_user_data] = ""

    # AWS SSH Keypair.
    #knife[:aws_ssh_key_id] = ""

The additional commented lines can all be passed to the `knife ec2 server create` command through its options, see `--help` for full options list.

Launching Instances
---------------------

Launch instances using knife-ec2's "server create" command. This command will do the following:

1.  Create an instance in EC2 using the options supplied to the command,
    and in the knife.rb file.
2.  Wait for the instance to be available on the network, and then wait
    until SSH is available.
3.  SSH to the instance as the specified user (see command-line
    options), and perform a "`knife bootstrap`," which is a built-in
    knife plugin that installs Chef and configures it for the Chef
    Server.
4.  Run chef-client with a specified run list, connecting to the Chef
    Server configured in `knife.rb`.

In this example, we're going to use an Ubuntu 12.04 AMI provided by Canonical in the default region and availability zone (us-east-1, us-east-1d. We'll use the default instance size (m1.small). We must specify the user that we'll connect with SSH (`-x ubuntu`), because it is not the default (root). We also specify the AWS SSH keypair (`-S jtimberman`). As a simple example, we'll set up an Apache Web Server with Opscode's `apache2` cookbook with a simple run list (`-r 'recipe[apt],recipe[apache2]'=), and use the =apt` cookbook to ensure the APT cache is updated. Then, we specify the security groups so the right firewall rules are opened (`-G default,www`).


`knife ec2 server create -x ubuntu -I ami-9a873ff3 -S jtimberman -G default,www -r 'recipe[apt],recipe[apache2]'`

The first thing this command does is talk to the EC2 API and provision a new instance.

    Instance ID: i-ABCDEFGH
    Flavor: m1.small
    Image: ami-9a873ff3
    Region: us-east-1
    Availability Zone: us-east-1d
    Security Groups: default
    Tags: {"Name"=>"i-f6d35a88"}
    SSH Key: jtimberman

    Waiting for server..........................
    Public DNS Name: ec2-XYZ-XYZ-XYZ-XYZ.compute-1.amazonaws.com
    Public IP Address: XYZ.XYZ.XYZ.XYZ
    Private DNS Name: ip-AB-AB-AB-AB.ec2.internal
    Private IP Address: AB.AB.AB.AB

    Waiting for sshd...done
    Bootstrapping Chef on ec2-XYZ-XYZ-XYZ-XYZ.compute-1.amazonaws.com


The "Bootstrap" Process
-----------------------

What follows will be the output of the [knife bootstrap process](http://docs.opscode.com/knife_bootstrap.html). That is, it installs Chef, and then runs `chef-client` with the specified run list.


    INFO: *** Chef 10.16.2 ***
    INFO: Client key /etc/chef/client.pem is not present - registering
    INFO: Setting the run_list to ["recipe[apt]", "recipe[apache2]"] from JSON
    INFO: Run List is [recipe[apt], recipe[apache2]]
    INFO: Run List expands to [apt, apache2]
    INFO: Starting Chef Run for i-ABCDEFGH
    SNIP: a bunch of chef run output!
    INFO: service[apache2] restarted
    INFO: Chef Run complete in 67.659549 seconds

The registration step is where the "validation" key is used to create a new client key for this instance. On the Chef Server:

    % knife client list
      i-ABCDEFGH
      YOUR_ORGNAME-validator

On the EC2 instance:

    $ ls /etc/chef
    client.pem  client.rb  first-boot.json  ohai  validation.pem

The `client.pem` file was created by the registration. We can safely delete the `validation.pem` file now, it is not needed, and there's actually a [recipe for that](https://github.com/opscode-cookbooks/chef-client/blob/master/recipes/delete_validation.rb).

The `client.rb` looks like this:

    log_level        :info
    log_location     STDOUT
    chef_server_url  "https://api.opscode.com/organizations/YOUR_ORGNAME"
    validation_client_name "YOUR_ORGNAME-validator"
    node_name "i-ABCDEFGH"

The `chef_server_url` and `validation_client_name` came from the `knife.rb` file above. The node name came from the instance ID assigned by EC2. Node names on a Chef Server must be unique, EC2 instance IDs are unique, whereas the FQDN (Chef's default here) may be recycled from
terminated instances.

The `ohai` directory contains hints for EC2. This is a new feature of the knife-ec2 plugin and ohai, to help better identify cloud instances, since certain environments make it difficult to auto-detect (including EC2 VPC and Openstack).

Now that the instance has finished Chef, it has a corresponding node object on the Chef Server.

    % knife node show i-ABCDEFGH
    Node Name:   i-ABCEDFGH
    Environment: _default
    FQDN:        ip-AB-AB-AB-AB.ec2.internal
    IP:          XYZ.XYZ.XYZ.XYZ
    Run List:    recipe[apt], recipe[apache2]
    Roles:
    Recipes:     apt, apache2
    Platform:    ubuntu 12.04
    Tags:


In this output, the FQDN is the private internal name, but the IP is the public address. This is so when viewing node data, one can copy/paste the public IP easily.

Managing Instance Lifecycle
---------------------------

There are many strategies out there for managing instance lifecycle in Amazon EC2. They all use different tools and workflows. The knife-ec2 plugin includes a simple "purge" option that will remove the instance from EC2, and if the node name in Chef is the instance ID, will remove
the node and API client objects from Chef, too.

    knife ec2 server delete -y --purge i-ABCDEFGH

Conclusion
----------

AWS EC2 is a wonderful environment to spin up new compute quickly and easily. Chef makes it even easier than ever to configure those instances to do their job. The scope of this post was narrow, to introduce some of the concepts behind the knife-ec2 plugin and how the bootstrap process
works, and there's much more that can be learned. 

Head over to the [Chef Documentation](http://docs.opscode.com/) to read more about how Chef works. 

Find cookbooks shared by others on the [Chef Community Site](http://community.opscode.com/). 

If you get stuck, the community has great folks available via the [IRC channels](http://community.opscode.com/chat) and [mailing lists](http://lists.opscode.com/).
