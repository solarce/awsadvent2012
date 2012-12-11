Options for Automating AWS
--------------------------

As we've seen in previous posts, [boto]() and [cloudformation]() are both options for helping automate your AWS resources, and can even compliment each other. 

But not everyone will want to use Amazon's CFN (which we covered in depth in the [day 6 post]()) or a Python library, so I thought we'd explore some of the options for automating your usage of AWS, starting with language libraries, then looking at some of the more popular SaaS offerings.

Python - boto, libcloud
-----------------------

Python has a few options for libraries. The most actively developed and used one's I've seen are [boto]() and [libcloud]()

__Boto__

__libcloud__


Ruby - fog, awsgem, knife
-------------------------

The main Ruby options seem to be [Fog]() and the [aws-sdk]() gem, for libraries, and [Opscode Chef's]() [knife]() tool also has nice support for AWS (which is built on top of Fog).

__Fog__

__aws-sdk__


http://aws.amazon.com/articles/8621639827664165


__knife__



Java - jclouds, AWS SDK for Java
--------------------------------

The Java world has a number of options, including [jclouds]() and the official [SDK for Java]()

http://aws.amazon.com/sdkforjava/

PHP - AWS SDK for PHP
---------------------

The only PHP full featured PHP library I could find was the official [SDK for PHP]()

http://aws.amazon.com/sdkforphp/

JavaScript - AWS SDK for Node.JS, AWSLib
--------------------------------

http://aws.amazon.com/sdkfornodejs/

https://github.com/livelycode/aws-lib

SaaS offerings
--------------

__RightScale__

__Ylastic__

__Enstratus__