#!/usr/bin/env python

# creates two ebs volumes and attaches them to an instance
# assumes you know the instance-id

import boto.ec2
import time

INSTANCE_ID="i-0c7abe3e"
REGION="us-west-2"
VOLUME_SIZE="5" # in gigabytes
VOLUME_AZ="us-west-2a" # should be same as instance AZ

# adjust these based on your instance types and number of disks
VOL1_DEVICE="/dev/sdh"
VOL2_DEVICE="/dev/sdi"

c = boto.ec2.connect_to_region(REGION)

# create your two volumes
VOLUME1 = c.create_volume(VOLUME_SIZE, VOLUME_AZ)
time.sleep(5)
print "created", VOLUME1.id
VOLUME2 = c.create_volume(VOLUME_SIZE, VOLUME_AZ)
time.sleep(5)
print "created", VOLUME2.id

# attach volumes to your instance
VOLUME1.attach(INSTANCE_ID, VOL1_DEVICE)
time.sleep(5)
print "attaching", VOLUME1.id, "to", INSTANCE_ID, "as", VOL1_DEVICE
VOLUME2.attach(INSTANCE_ID, VOL2_DEVICE)
time.sleep(5)
print "attaching", VOLUME2.id, "to", INSTANCE_ID, "as", VOL2_DEVICE
