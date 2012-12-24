Monitoring and AWS
------------------

A critical part of any application infrastructure is monitoring. Now monitoring can mean a lot of things to different people, but for the purposes of this post we're going to define monitoring as two things

1. Collecting metrics data to look at performance over time
2. Alerting on metrics data based on thresholds

Let's take a look at some of the tools and services available to accomplish this and some of their unique capabilities. 

There are certainly many many options for this, as a search for ["aws monitoring"](https://www.google.com/search?q=aws+monitoring) will reveal, but I am going to focus on a few options that I am familiar with and see as representing the various classes of options available.

Amazon CloudWatch
-----------------

[Amazon CloudWatch](http://aws.amazon.com/cloudwatch/) is of course the first option you may think when your using AWS resources for your application infrastructure as it's already able to to automatically provide you with metric data for most AWS services.

CloudWatch is made up of three main components:

* [metrics](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/GettingStartedGuide/PublishMetrics.html): metrics are data points that are stored in a time series format.
* [graphs](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/GettingStartedGuide/ViewGraphs.html): which are visualizations of metrics over a time period.
* [alarms](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/AlarmThatSendsEmail.html): an alarm watches a single metric over a time period you specify, and performs one or more actions based on the value of the metric relative to a given threshold over a number of time periods

Currently CloudWatch has built-in support for the following services:

* AWS Billing
* Amazon DynamoDB
* Amazon ElastiCache
* Amazon Elastic Block Store
* Amazon Elastic Compute Cloud
* Amazon Elastic MapReduce
* Amazon Relational Database
* Amazon Simple Notification Service
* Amazon Simple Queue Service
* Amazon Storage Gateway
* Auto Scaling
* Elastic Load Balancing

CloudWatch provides you with the API and storage to be able to [monitor](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/US_GetStatistics.html) and [publish](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/publishingMetrics.html) metrics for these AWS services, as well as adding your own [custom data](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html), through many interfaces, including [CLI tools](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/choosing_your_cloudwatch_interface.html#UsingTheCLI), [An API](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/choosing_your_cloudwatch_interface.html#Using_Query_API), or via many [language libraries](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/choosing_your_cloudwatch_interface.html#using-libraries). They even provide some [sample monitoring scripts](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/mon-scripts.html) for collecting OS information for Linux and Windows.

Once your metric data is being stored by CloudWatch, you're able to [create alarms](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/AlarmThatSendsEmail.html) which use [AWS SNS](http://docs.amazonwebservices.com/AmazonCloudWatch/latest/DeveloperGuide/US_SetupSNS.html) to send alerts via email, SMS, or posting to another web service.

Finally, you're able to visualize these metrics in various ways through the [AWS console](https://console.aws.amazon.com/cloudwatch/home).

[CloudWatch pricing](http://aws.amazon.com/pricing/cloudwatch/) is straightforward. You pay per custom metric, per alarm, per API request, all on a monthly basis, and _Basic Monitoring_ metrics (at five-minute frequency) for Amazon EC2 instances are free of charge, as are all metrics for Amazon EBS volumes, Elastic Load Balancers, and Amazon RDS DB instances.

Boundary
--------

[Boundary](http://boundary.com/why-boundary/) is a startup based out of San Francisco which takes an interesting approach to monitoring. _Caveat, I am friends with a few of the folks there and very excited about what they're doing._

Boundary is a hosted offering who's goal is to provide in-depth application monitoring by looking at things from the point of view of _the network_. The service works by having you deploy an agent they call a _meter_ to each your servers, they currently support a variety of Linux distributions and Window 2008 server. These meters send [IPFIX](http://en.wikipedia.org/wiki/IP_Flow_Information_Export) data back to Boundary's hosted platform, where the data is processed and stored.

The idea behind Boundary is that by looking at the data from the network, in real time, you're able to quickly see patterns in the flow of data in and out of your infrastructure and between the tiers within it in a way that hasn't been as easily done with traditional monitoring tools that are looking at OS metrics, SNMP data, etc. And by being able to annotate this data and monitor for changes, you can create a comprehensive and detailed real time and long term view into your infrastructure.

You're then able to [visualize your data](http://boundary.com/ways/#way-4) in [various ways](http://boundary.com/ways/#way-11), including [annotating and overlaying](http://boundary.com/ways/#way-13) it or adding your own [custom data](http://boundary.com/ways/#way-21). You're then able to have [alerts](http://boundary.com/ways/#way-23) sent by email natively or in a variety ways through their supported integration with [PagerDuty](http://www.pagerduty.com). Some more details on how you're able to use Boundary is laid out in their [30 Days to Boundary](http://boundary.com/ways/) page.

[Boundary's pricing](http://boundary.com/pricing/) is simple. It starts with a Free plan that lets you store up to 2GB of metric data/day. Paid plans begin at $199 US/month for commercial support, higher daily storage limits, flexible long term data storage options.

Boundary even has a couple good resources focused on how they're a good fit for when you're using AWS, including a video, [See Inside the Amazon EC2 Black Box](http://youtu.be/3I1JThRJvuc) and a PDF, [Optimizing Performance in Amazon EC2](http://boundary.com/wp-content/uploads/2012/08/Boundary-for-Amazon-Ec2-Solution-Brief.pdf), that are worth reviewing.


Datadog
-------

[Datadog](http://www.datadoghq.com/product/) is a hosted offering based out of New York City that aims to give you a unified place to store metrics, events and logs from your infrastructure _and_ third party services, to visualize this data, and alert on it, as well as discuss and collaborate on this data.

Datadog works by having you installing [an agent](http://help.datadoghq.com/kb/general/getting-started), which they currently support running on a variety of Linux distributions, Windows, OSX, and SmartOS. They also support [integration](http://www.datadoghq.com/integrations/) with a variety of open source tools, applications, languages, some third party services.

Once you've installed the agent and configured your desired integations, you'll begin seeing events and metrics flow into your account. You're able to build your own [agent based checks](http://docs.datadoghq.com/guides/agent_checks/) and [service checks](http://docs.datadoghq.com/guides/services_checks/) and do custom integration through a number of [libraries](http://docs.datadoghq.com/libraries/).

From there you can beginning visualizing and using your data by making [custom dashboards](http://www.datadoghq.com/product/product?goto=fb2) and then creating [alerts](http://www.datadoghq.com/alerts/) which can be sent via email or in a variety ways through their supported integration with [PagerDuty](http://www.pagerduty.com).

[Datadog's pricing](http://www.datadoghq.com/pricing/) starts with a free plan that includes 1 day retention and 5 hosts. Paid plans start at $15/host/month for up to 100 hosts with one year retention, alerts, and email support.

Sensu
-----

Not everyone wants to utilize a hosted serviced and there are a number of open source tools for building your own monitoring solution.

The up and coming tool in this space is [Sensu](https://github.com/sensu). Sensu is an open source project that is sponsored by [Sonian](http://www.sonian.com/about/) and has a thriving developer and user community around it. Sensu was built by Sonian out of [their need for a flexible solution](http://portertech.ca/2011/11/01/sensu-a-monitoring-framework/) that could handle how they dynamically scale their infrastructure tiers up and down on various public cloud providers, starting with AWS.

Sensu's goal is to be a monitoring framework that let's you build a scalable solution to fit your needs. It is built from the following components:

* The server, which aggregates data from the clients
* The clients, which run checks
* The API service
* RabbitMQ, which is the message bug that glues everything together

The various Sensu components are all written in Ruby and open source. Sensu supports running checks written in Ruby, as well as existing Nagios checks.

This excellent [getting started post](http://joemiller.me/2012/01/19/getting-started-with-the-sensu-monitoring-framework/) by [Joe Miller](https://twitter.com/miller_joe) sums Sensu up nicely.

> Sensu connects the output from “check” scripts run across many nodes with “handler” scripts run on Sensu servers. Messages are passed via [RabbitMQ](http://www.rabbitmq.com/). Checks are used, for example, to determine if Apache is up or down. Checks can also be used to collect metrics such as MySQL statistics. The output of checks is routed to one or more handlers. Handlers determine what to do with the results of checks. Handlers currently exist for sending alerts to Pagerduty, IRC, Twitter, etc. Handlers can also feed metrics into [Graphite](http://graphite.wikidot.com/), [Librato](https://metrics.librato.com/), etc. Writing checks and handlers is quite simple and can be done in any language.

Nagios
------

[Nagios](http://library.nagios.com/library/products/nagioscore/manuals/) is the granddaddy of open source monitoring tools. It's primarily a server service you run that it watches hosts and services that you specify, alerting you when things go bad and when they get better. It supports a variety of checks for most services and software, as well as the ability to write your own. You'll find checks, scripts, and extensions for Nagios for pretty much anything you can think of.

For metrics and alerting there are good tools for integrating [with Graphite](http://datacratic.com/site/blog/statsd-graphite-and-nagios) and [PagerDuty](http://www.pagerduty.com/docs/guides/nagios-integration-guide).

Conclusion
----------

There are a number of hosted and open source solutions available to match your infrastructure's monitoring needs. While this post hasn't covered them all, I hope you've gotten a nice overview of some of options and some food thought when considering how to gather the metrics and data needed to run an application on AWS and stay alerted to the changes and incidents that are important to you.

If you're interested in learning more about open source monitoring, you should watch [The State of Open Source Monitoring](http://vimeo.com/51120680) by [Jason Dixon](http://www.twitter.com/obfuscurity).

If you're interested in the future of monitoring, you should keep an eye on the upcoming [Monitorama](http://monitorama.com/) conference coming up in March 2013.