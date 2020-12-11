# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "generic/debian10"

  config.vm.hostname = "demi1"
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  config.vm.network "public_network", mac: "52:54:00:d3:59:5c", bridge: "enp1s0", dev: "enp1s0"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<~SHELL
      ip route del default
      ip route add default via 192.168.16.1 dev eth1
      echo 192.168.16.11 metal1 >> /etc/hosts
      echo net.ipv6.conf.all.disable_ipv6=0 > /etc/sysctl.d/enable_ipv6.conf
      sysctl -p /etc/sysctl.d/enable_ipv6.conf
      passwd --delete root
      passwd --delete vagrant
      useradd --create-home --user-group --shell /bin/bash ansible
      useradd --create-home --user-group --shell /bin/bash lemon
      useradd --create-home --user-group --shell /bin/bash andrei
      useradd --create-home --user-group --shell /bin/bash char
      sudo -u ansible ssh-keygen -f /home/ansible/.ssh/id_rsa -t rsa -q -N '' 
      cat /etc/sudoers.d/vagrant | sed 's/vagrant/ansible/' > /etc/sudoers.d/ansible 
      cat <<EOF | sudo -u ansible tee /home/ansible/.ssh/authorized_keys
      ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxjlhGBSacO13z15L3YMDq7PaH4cq2orYFDUc/Bv6gmPl9MvO2G0cwscLhAerNlllmSFDUBJl0TEOdKhtUYlLcwEDZ2bCFdzNGAJUmH2HtXOGvrlQNk1e1dkNUnlvAO8b+5mqn/kxYw7I9mdKAyG4r3kWmvskoUhOkBKmjezIoiYC8PakO2RgBXSWaR+1DLnPqWE3++9xHiTWmtbdp+rXAitCjtqQitLIwZSen5o7A294ixEmQjkr+Te2bm8l5eVn/hnalzKPDmVeWgJvRWLapxN0F1D6rKtLcgB83pHAeQpezX93nKAsuqsrRe4hI1ZHtfkKVD2o+nHqYIQ+C9ydP ansible@metal1
      EOF
  SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
