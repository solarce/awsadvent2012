#!/usr/bin/env python

import boto.s3

REGION="us-west-2"
BUCKET="mybucket"

c = boto.s3.connect_to_region(REGION)

bucket = c.get_bucket(BUCKET)

from boto.s3.lifecycle import Lifecycle, Transition, Rule
to_glacier = Transition(days=30, storage_class='GLACIER')
rule = Rule('ruleid', 'logs/', 'Enabled', transition=to_glacier)

lifecycle = Lifecycle()
lifecycle.append(rule)

bucket.configure_lifecycle(lifecycle)

current = bucket.get_lifecycle_config()
print current[0].transition