#!/bin/bash

# all commands run as root because they're run via cloud-init and passed in as user-data

# install the omnibus client
true && curl -L https://www.opscode.com/chef/install.sh | bash

# make a directory for chefef stuff
mkdir /etc/chef

# grab our private key for talking to hosted chef
curl http://BUCKETNAME.s3.amazonaws.com/ORGNAME-validator.pem -pemo /etc/chef/ORGNAME-validator.pem

# grab a minimal client.rb for getting the chef-client registered
curl http://BUCKETNAME.s3.amazonaws.com/client.rb -o /etc/chef/client.rb

#kick off the first chef run
/usr/runbin/chef-client

