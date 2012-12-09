import boto.sns
import logging

logging.basicConfig(filename="sns-topic.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-west-2")

topicname = "adventtopic"

topicarn = c.create_topic(topicname)

print topicname, "has been successfully created with a topic ARN of", topicarn
