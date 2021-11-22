Things required to set up the router as a loadbalancer:
* Port forwards: None
* Setup network: .16.1/24
  * Set static route on home's router
* Traffic rules:
  * Allow 16 to 15's router/nas/logs
  * Prevent 16 to LAN
* Upload `loadbalancer` script to cgi-scripts
* Upload `firewall.user` script to etc
* Install iptables, ip6tables, iptables-mod-ipopt
* Set dnsmasq domain: demi.lan
  * Set DNS forwarding on home's router as well
* Set up static leases for metal, demi, and kube hosts
  * Example: demi1 52:54:00:D3:59:5C 192.168.16.21 none none 21
