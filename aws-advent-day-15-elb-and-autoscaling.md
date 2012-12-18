Using ELB and Auto-Scaling
--------------------------

Load balancing is a critical piece of any modern web application infrastructure and Amazon's [Elastic Load Balancer (ELB)](http://aws.amazon.com/elasticloadbalancing/) service provides an API driven and integrated solution for load balancing when using AWS services. Building on top of Amazon's [CloudWatch](http://aws.amazon.com/cloudwatch/) monitoring and metrics solution, and easily coupled with ELB, Amazon's [Auto-Scaling](http://aws.amazon.com/autoscaling/) service provides you with the ability to dynamically scaling parts of your web application infrastructure on the fly and based on performance or user demand.

__Elastic Load Balancer__

ELB is a [software load balancer solution](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/SvcIntro_arch_workflow.html) that provides you with public IPs, SSL terminations, and the ability to do layer 4 and 7 load balancing, with session stickyness, as needed. Managed through the [AWS console](https://console.aws.amazon.com/console/home), [CLI tools](http://aws.amazon.com/developertools/2536), or the[ELB API](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/APIReference/Welcome.html). All while paying by the hour, only for the resources and bandwidth used.

__Auto-Scaling__

Auto-Scaling lets you define CloudWatch metrics for dynamically scaling EC2 instances up and down, completely automatically. You're able to utilize On-Demand or Spot instances, inside or out of your VPC for the scaling and it easily couples with ELB to allow auto-scaled instances to begin serving traffic for web applications. Managed through the [AS CLI tools](http://aws.amazon.com/developertools/2535) or the[AS API](http://docs.amazonwebservices.com/AutoScaling/latest/APIReference/Welcome.html). All while paying by the hour, only for the CloudWatch metrics used. You're also able to use [AWS SNS] to get alerted as auto-scaling policies take actions.

Getting Started with ELB
------------------------

ELB is composed of [ELB instances](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/CreateLoadBalancer.html). An _ELB instance_ has the following elements:

* [Listeners](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/DefineLoadBalancer.html)
* [Health Checks](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/ConfigureHealthCheck.html)
* [EC2 instances](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/US_DeReg_Reg_Instances.html)

To get started with ELB you'll build an ELB instance

1. Login to the [AWS console](https://console.aws.amazon.com/console/home)
2. Click Load Balancers
3. On the DEFINE LOAD BALANCER page, make the following selections:
4. Enter a name for your load balancer (e.g., MyLoadBalancer).
5. Leave CreateLB inside set to EC2 because in this example you'll create your load balancer in Amazon EC2. The default settings require that your Amazon EC2 HTTP servers are active and accepting requests on port 80.
6. On the CONFIGURE HEALTH CHECK page of the Create a New Load Balancer wizard, set the following configurations:
7. Leave Ping Protocol set to its default value of HTTP.
8. Leave Ping Port set to its default value of 80.
9. In the Ping Path field, replace the default value with a single forward slash ("/"). Elastic Load Balancing sends health check queries to the path you specify in Ping Path. This example uses a single forward slash so that Elastic Load Balancing sends the query to your HTTP server's default home page, whether that default page is named index.html, default.html, or a different name.
10. Leave the Advanced Options set to their default values.
11. On the ADD INSTANCES page, check the boxes in the Select column to add instances to your load balancer.
12. On the Review page of the Create a New Load Balancer wizard, check your settings. You can make changes to the settings by clicking the edit link for each setting.
13. Now that you've made your configuration choices, added your instances, reviewed your selections, and have clicked Create, you're ready to create your load balancer.
14. After you click Create button in the REVIEW page, a confirmation window opens. Click Close. When the confirmation window closes, the Load Balancers page opens. Your new load balancer now appears in the list.
15. You can test your load balancer after you've verified that at least one of your EC2 instances is InService. To test your load balancer, copy the DNS Name value that is listed in the Description tab and paste it into the address field of an Internet-connected web browser. If your load balancer is working, you will see the default page of your HTTP server.

Now that you've created an ELB instance, some of things you may want to do could include:

* [Add or Remove EC2 instances](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/US_DeReg_Reg_Instances.html)
* [Add additional listeners](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/us-add-listener.html)
* [Deploy an ELB instance in a VPC](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/UserScenariosForVPC.html)
* [Enabling SSL for your ELB instance](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/US_UpdatingLoadBalancerSSL.html)
* [Using Custom Domains with your ELB instance](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/using-domain-names-with-elb.html)
* [Using Sticky Sessions with your ELB instance](http://docs.amazonwebservices.com/ElasticLoadBalancing/latest/DeveloperGuide/US_StickySessions.html)


Getting Started with Auto-Scaling
---------------------------------

Auto-Scaling is built from two things, a _launch configuration_ and an _auto-scaling group_.

To build an auto-scaling configuration, do the following

1. Download and [Install](http://docs.amazonwebservices.com/AutoScaling/latest/GettingStartedGuide/SetupCLI.html) the AS CLI tools
2. [Create a launch configuration](http://docs.amazonwebservices.com/AutoScaling/latest/GettingStartedGuide/CreateASGroup.html#create-launch-config), e.g. `as-create-launch-config MyLC --image-id ami-2272864b --instance-type m1.large`
3. [Create an Auto-Scaling group](http://docs.amazonwebservices.com/AutoScaling/latest/GettingStartedGuide/CreateASGroup.html#create-auto-scaling-group), e.g. `as-create-auto-scaling-group MyGroup --launch-configuration MyLC --availability-zones us-east-1a --min-size 1 --max-size 1`
4. You can list your auto-scaling group with `as-describe-auto-scaling-groups --headers`

At this point you have a basic auto-scaling group. 

To make this useful you'll probably want to do some of the following

* [Make instance termination policies](http://docs.amazonwebservices.com/AutoScaling/latest/DeveloperGuide/us-termination-policy.html)
* [Utilize Alarms and Load Balancing](http://docs.amazonwebservices.com/AutoScaling/latest/DeveloperGuide/US_SetUpASLBApp.html)
* [Use AS to launch Spot instances](http://docs.amazonwebservices.com/AutoScaling/latest/DeveloperGuide/US-SpotInstances.html)
* [Using Auto-Scaling and VPC](http://docs.amazonwebservices.com/AutoScaling/latest/DeveloperGuide/autoscalingsubnets.html)

Conclusion
----------

In conclusion, ELB and Auto-Scaling provide a number of options for managing and scaling your web application infrastructure based on traffic growth and user demand and letting easily mix and match them with other AWS services.