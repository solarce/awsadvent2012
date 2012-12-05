Getting Started with Boto
-------------------------

[Boto](https://github.com/boto/boto) is a Python libary that provides you with an easy way to interact with and automate using various Amazon Web Services.

If you're familiar with Python or interested in learning it, in conjunction with learning and use AWS, you won't find a better option than Boto.

Installing
----------

Installing boto is very straightforward, assuming your using an OS with [pip]() installed. If you do not currently have pip, then [do that first](http://www.pip-installer.org/en/latest/installing.html).

Once you have pip, the following command will get you up and running.

`pip install boto`

Basic configuration
-------------------

This configuration assumes you've already created an AWS account and obtained your [API Key]() and [Secret Access Key]() from [IAM]() in the [AWS console]()

With those in hand, you'll want to create a [.boto file](http://docs.pythonboto.org/en/latest/boto_config_tut.html) in your home directory and populate it with the secrets. 

* Example _.boto_:

	`[Credentials]`

	`aws_access_key_id = <your access key>`

	`aws_secret_access_key = <your secret key>`

* There are some additional configurations you can set, as needed, for debugging, local proxies, etc, as shown below

	`[Boto]`

	`debug = 0`
	
	`num_retries = 10`

	`proxy = myproxy.com`

	`proxy_port = 8080`
	
	`proxy_user = foo`
	
	`proxy_pass = bar`

Using boto with EC2
-------------------

Now that you have a basic [.boto file](http://docs.pythonboto.org/en/latest/boto_config_tut.html), you can begin using boto with AWS resources.

The most likely place to start is connecting to EC2 and making an instance, which can be done with a few short lines of code.

_ec2.py_

`



