AWS Direct Connect
------------------

Today's post on [AWS Direct Connect](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/Welcome.html) is a contribution by [Benjamin Krueger](https://twitter.com/blueben), who is a Site Reliability Engineer for Sourcefire, Inc and is presently working with a highly talented team to build a flexible hybrid cloud infrastructure. 

He enjoys a delicious cup of buzzword soup, and isn't afraid to SOA his cloud with API driven platform metrics. His event streams offer high availability processing characteristics. Turbo Encabulator.


Deck the halls with single-mode fiber
-------------------------------------

I wish I could have my cake and eat it too.

Whether you are a fan or critic, the world of cloud computing has undeniably changed how many of us build and operate the services we offer. Also undeniable, however, is the fact that the reliability of your access to resources in the cloud is limited by the reliability of all the networks in between. In the networking world, one way that ISPs, carriers, and content providers often side-step this issue is by participating in Internet Exchanges; physical network meet up points where participants exchange network traffic directly between their respective networks. Another form of this is through direct network peering agreements where two parties maintain a direct physical network connection between each other to exchange traffic.

While the cloud offers lots of benefits, sometimes it just doesn't make sense to run your entire operation there. You can't run your own specialized network appliances in the cloud, for example. Perhaps your requirements specify a level of hardware control that can't be met by anything other than an in-house datacenter. Maybe the cost-benefit of available cloud server instances makes sense for some workloads but not for others. Sure, you can write off the cloud entirely but wouldn't it be nice if you could build a hybrid solution and get a network connection direct from your own datacenter or home office to your cloud provider's network? If you're an Amazon Web Services customer then you can do this today with AWS Direct Connect. This article won't be a howto cookbook but will outline what Direct Connect is and how you can use it to improve the reliability and performance of your infrastructure when taking advantage of the benefits of cloud services.

AWS Direct Connect service.
---------------------------

The AWS Direct Connect service lets you establish a network link, at 1Gb or 10Gb, from your datacenter to one of seven Amazon regional datacenters across the globe. At the highest level, you work with your infrastructure provider to establish a network link between your datacenter and an AWS Direct Connect Location. Direct Connect Locations are like meet up points. Each is located in physical proximity to an Amazon region, and are the point where direction connections are brought in to Amazon's network for that region.

__AWS Direct Connect Locations__

<table>
	<tr>
		<td><strong>Data Center Facility</strong></td>
		<td><strong>AWS Region</strong></td>
	</tr>
    <tr>
        <td>CoreSite 32 Avenue of the Americas, N</td>
        <td>US East (Virginia) Region </td>
    </tr>
    <tr>
        <td>CoreSite One Wilshire & 900 North Alameda, LA  </td>
        <td>US West (Northern California) Region </td>
    </tr>
    <tr>
        <td>Equinix DC1 - DC6 & DC10 </td>
        <td>US East (Northern Virginia) Region </td>
    </tr>
    <tr>
        <td>Equinix SV1 and SV5 </td>
        <td>US West (Northern California) Region</td>
    </tr>
    <tr>
        <td>Equinix, SG2 </td>
        <td>Asia Pacific (Singapore) Region </td>
    </tr>
    <tr>
        <td>Equinix, TY2 </td>
        <td>Asia Pacific (Tokyo) Region </td>
    </tr>
    <tr>
        <td>TelecityGroup, London Docklands’ </td>
        <td>EU West(Ireland) Region </td>
    </tr>
    <tr>
        <td>Terremark NAP do Brasil, Sao Paulo </td>
        <td>South America (Sao Paulo) Region </td>
    </tr>
    <tr>
        <td>Equinix, SY3 </td>
        <td>Asia Pacific (Sydney) Region </td>
    </tr>
</table>


As an illustration, let's explore a hypothetical Direct Connect link from a New Jersey datacenter to Amazon's US-East region. Amazon maintains Direct Connect Locations for their US-East Northern Virginia region at CoreSite in New York City, and seven Equinix data centers in Northern Virginia. Being in New Jersey, it makes sense for us to explore a connection to their CoreSite location in New York. Since you don't already have a presence in CoreSite, you would make arrangements to rent a cage and collocate. Then you would have to make arrangements, usually with a telco or other network infrastructure provider, to create a link between your datacenter and your gear in CoreSite. At that point, you can begin the process to cross-connect between your CoreSite cage and [Amazon's CoreSite cage](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/Colocation.html).

The example I just outlined has quite a few drawbacks. We need to interface with a lot of companies and sign a lot of contracts. That necessarily means quite a bit of involvement from your executive management and legal counsel. It also requires a significant investment of time and Capex, as well as ongoing Opex. Is there anything we can do to make this process simpler and more cost-effective?

__An AWS Direct Connect Layout__

![](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/images/ADC_Connection_Map_v3_screen.png)

As it turns out, there is something we can do. Amazon has established a group of what they call [APN Technology and Consulting Partners](http://aws.amazon.com/directconnect/partners/). That's quite a mouthful, but it boils down to a group of companies with can manage many of the details involved in the Direct Connect process. In the example layout above, we work with an APN Partner who establishes a link between our datacenter and the Direct Connect Location. They take care of maintaining a presence there, as well as the details involved in interfacing with Amazon's cage. The end result is a single vendor helping us establish our Direct Connect link to Amazon.

So what's this gonna cost me?
-----------------------------

At the time of this publication, Amazon's charges [$0.30 per port-hour for 1Gb connections and $2.25 per port-hour for 10Gb connections](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/pricing.html). Since the ports are always on while you use the service, that works out to approximately $220/mo for 1Gb and $1650/mo for 10Gb. In addition, Amazon charges $0.03 per GB of outbound transfers while inbound transfers are free. That means a Direct Connect link makes the most sense for pushing large quantities of data towards Amazon. This works out well for scenarios where systems in the cloud make small requests to systems in your datacenter which then return larger results.

Costs when dealing with an APN Partner can vary. In my own environment, the vendor costs approximately $3k/mo. The vendor takes care of the connection between our North Virginia datacenter and Amazon's Equinix Direct Connect Location, and we get a single-mode fiber drop straight into our cage. All we have to do is plug it in to our router. For more complex links, costs will obviously be higher. You could direct connect your Toronto datacenter to Amazon through CoreSite in New York but with getting fiber out of your cage, working with a network carrier for the trip between cities, cage rental, and cross connect charges, don't be surprised if the bill is significant!

Get your packets runnin'
------------------------

Once you have a physical path to Amazon, you need to plug it in to something. Amazon requires that your router support [802.1Q VLANs](http://www.ieee802.org/1/pages/802.1Q.html), [BGP](http://www.bgp4.as/), and [BGP MD5 authentication](http://evilrouters.net/2009/07/10/configuring-md5-authentication-for-bgp-peers/). While this often means using a traditional network router from a company like Cisco or Juniper, you could also build a router using Linux and a BGP implementation like [OpenBGP](http://www.openbgpd.org/) or [Zebra](http://lartc.org/howto/lartc.dynamic-routing.bgp.html). If you have an ops team, but the idea of BGP makes you shiver, don't fret. Once you give them some details, Amazon will generate a sample configuration for common Cisco and Juniper routers.

To begin routing traffic to AWS public services over your Direct Connect link, you will need to create a [Virtual Interface](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/getstarted.html#createvirtualinterface) in Amazon's configuration console. You only need a few pieces of information to set this up: A VLAN number, a [BGP ASN](http://www.inetdaemon.com/tutorials/internet/ip/routing/bgp/autonomous_system_number.shtml), your router's peer IP address (which Amazon will provide), Amazon's peer IP address (also provided), and the network prefixes that you want to advertise. Some of this is straight-forward, and some less so. If you do not have a BGP ASN then you can choose an arbitrary number between 64512 and 65534, which is a range of BGP ASNs reserved by IANA similar to RFC1918 address space. The prefix is a public address block which Amazon will know to route over your virtual interface; This could be as small as a /32 for a NAT server that your systems live behind. It should be noted that at this time, Direct Connect does not support IPv6.

Amazon has authored some excellent documentation for most of their AWS services, and the process for [creating Virtual Interfaces is no exception](http://docs.amazonwebservices.com/directconnect/latest/UserGuide/getstarted.html#createvirtualinterface). Your configuration may require some subtle changes, and of course you should never promote any system to production status without fully understanding the operational and security consequences of its configuration. 

But once you've reached that point and your virtual interface is online, Amazon will begin routing your packets over the link and you now have a direct connection straight in to Amazon's network!

So what does a hybrid infrastructure look like?
-----------------------------------------------

In addition to using Direct Connect to access AWS public services, you can also use it to run your own infrastructure on Amazon's platform. One of the most polished and well-supported ways to do this is by using Amazon's Virtual Private Cloud service. A VPC environment allows you to take your server instances out of Amazon's public network. If you are familiar with Amazon's EC2 platform, you will recall that server instances live on a network of private address space alongside every other EC2 customer. VPC takes that same concept, but puts your instances on one or more private address spaces of your choosing by themselves. Additionally, it offers fine-grained control over which machines get NAT to the public internet, which subnets can speak to each other, and other routing details. Another benefit offered by VPC is the ability for your Direct Connect Virtual Interface to drop straight on to your VPC's private network. This means that the infrastructure in both your datacenter and Amazon VPC can live entirely on private address space, and communicate directly. Your network traffic never traverses the public internet. In essence, your VPC becomes a remote extension of your own datacenter.

When to use all this?
---------------------

So what kind of situations can really benefit from this kind of hybrid infrastructure? There are myriad possibilities, but one that might be a common case is to take advantage of Amazon's flexible infrastructure for service front-ends while utilizing your own hardware and datacenter for IO intensive or sensitive applications. In our hypothetical infrastructure, taking advantage of Amazon's large bandwidth resources, ability to cope with DDoS, and fast instance provisioning, you bring up new web and application servers as demand requires. This proves to be cost effective, but your database servers are very performance sensitive and do not cope well in Amazon's shared environment. Additionally, your VP really wants the master copy of your data to be on resources you control. Running your database on Amazon is right out, but using Direct Connect your app servers can connect right to your database in your datacenter. This works well, but all of your read requests are traversing the link and you'd like to eliminate that. So you set up read slaves inside Amazon, and configure your applications to only send writes to the master. Now only writes and your replication stream traverse the link, taking advantage of Amazon's Direct Connect pricing and free inbound traffic.

How's it work?
--------------

So how well can Direct Connect perform? Here is an example of the latency between the router in my own datacenter in Northern Virginia, and the router on Amazon's US-East network. This is just about a best-case scenario, of course, and the laws of physics apply.

<pre>
#ping 1.1.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
!!!!!                
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/4 ms
</pre>

One millisecond, which is the lowest precision result our router provides! Due to a misconfiguration, I don't presently have throughput stats but when measured in the past we have been able to match the interface speed that the router is capable of. In other words, Direct Connect performs exactly as you would expect a fiber link between two locations would.

Wrapping up
-----------

There are caveats to using Direct Connect, especially in a production environment. Being a single line of fiber, your network path is exposed to a few single points of failure. These include your router, the fiber in between yourself and the Direct Connect Location, and the infrastructure between the Direct Connect Location and Amazon's regional datacenter. Additionally, Amazon does not offer an SLA on Direct Connect at this time and reserves the right to take down interfaces at their entry for maintenance. Because of this, Amazon recommends ensuring that you can fail over to your primary internet link or ordering a second Direct Connect link. If your requirements include low latency and high throughput, and failing over to your default internet provider link will not suffice, a second Direct Connect link may be justified.

While I've outlined Direct Connect's benefits for a single organization's hybrid infrastructure, that certainly isn't the only group who can take advantage of this service.  Hosting companies, for example, might wish to maintain Direct Connect links to Amazon datacenters so that their customers can take advantage of Amazon's Web Services in a low latency environment. Organizations with a traditional datacenter might use AWS as a low cost disaster recovery option, or as a location for off-site backup storage.

I hope this article has helped illuminate Amazon's Direct Connect service. Despite a few drawbacks this service is a powerful tool in the system administrator's toolbox, allowing us to improve the reliability and performance of our infrastructures while taking advantage of the benefits of Amazon's cloud platform. Hopefully we will soon start seeing similar offerings from other cloud providers. Perhaps there may even be dedicated cloud exchanges in the future, allowing direct communication between providers and letting us leverage the possibility of a truly distributed infrastructure on multiple clouds.


