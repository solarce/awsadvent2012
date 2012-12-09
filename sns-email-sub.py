import boto.sns
import logging

logging.basicConfig(filename="sns-email-sub.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-west-2")

topicarn = "arn:aws:sns:us-west-2:740810067088:adventtopic"
emailaddress = "you@you.you"

subscription = c.subscribe(topicarn, "email", emailaddress)

print subscription