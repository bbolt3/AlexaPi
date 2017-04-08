# This is a fork of AlexaPi that adds a network trigger as a dummy platform

Instead of wiring a button on Raspberry Pi's GPIO pins, I wanted to integrate a WiFi-based Amazon Dash Button as the switch to trigger Alexa.

### Check out the [Original Project](https://github.com/alexa-pi/AlexaPi) for details on initial setup and installation.

The UDP socket sits and listens for a user specified port, and if the IP is the IP specified in the configuration file, it will activate as a trigger. To get the Amazon Dash Button traffic to the network listener I configured this on the router as I didn't really want a Pi snooping on network traffic. Router used is a Mikrotik using RouterOS so implementation will vary based on router.

First step is register the dash button using the mobile application. When it gives the option to choose a product to associate with the dash button, you can cancel out. Next you'll want to identify the MAC address of the button on the router and assign it a static address. It would also be wise to assign the Raspberry Pi a static IP as well. On RouterOS, I went into DHCP Server option in the IP settings and set the lease to a very long lease and gave it a static address. If you configure it with a short lease, there's a good 4-5 second lag when the lease is established. Without dealing with the lease configuration it works very quickly.

![Screenshot](http://i.imgur.com/0CIgumy.png)

Next, I added a NAT firewall rule that takes all UDP traffic coming from my Dash Button and sends it to my Raspberry Pi on the port I have the network option on AlexaPi watching for traffic. 192.168.88.8 is my Dash Button and 192.168.88.5 is the Raspberry Pi.

![Screenshot](http://i.imgur.com/eIjI3LN.png)

That's all the settings that are needed on the router side to make this work. If you want to take the extra step of blocking all traffic from the Dash Button to the outside network, add a firewall rule that drops all traffic from that IP.

![Screenshot](http://i.imgur.com/BEJfSv4.png?1)

Then open config.yaml from the AlexaPi installation and enter the IP of the Pi and the port you want it to listen on. Then for the client IP enter the address that you've assigned to the Dash Button. 

Your Dash Button now should be able to trigger AlexaPi. There's a timeout period used since the button will attempt to send multiple requests and it should only be processed once per button press. 

