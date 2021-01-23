A firewall script and web page to control OpenWrt's routing to demi hosts. There
is no ansible file yet, as access to the router is denied for security reasons.

To install the files:

    scp loadbalancer openwrt-9-demi:/www/cgi-bin/
    scp firewall.user openwrt-9-demi:/etc/

To add and remove targets to the loadbalancer:

    curl http://openwrt-9-demi/cgi-bin/loadbalancer?add=192.168.16.21
    curl http://openwrt-9-demi/cgi-bin/loadbalancer?remove=192.168.16.22

The result will be a 400 for invalid requests, or 200 with a text message like:

    Target 192.168.16.21 added. Firewall reloaded successfully.
    
The result will be a 200 even if the firewall reloaded unsuccessfuly, so the
message should be checked as well.
