import boto.sns
import logging

logging.basicConfig(filename="sns-publish.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-west-2")

topicarn = "arn:aws:sns:us-west-2:740810067088:adventtopic"
message = "hello advent reader"
message_subject = "aws advent 2012"

publication = c.publish(topicarn, message, subject=message_subject)

print publication