# Description
A dynamic inventory plugin for Ansible which pings a given cidr network and adds hosts if there is a response to the ping. 

The name comes from addr being part of the nix command ipaddr but also a misspelling of 'ip adder' since this shit adds ips as hosts. Very Clever.   

# Usage
## Loading the module
It's just a normal inventory plugin. It needs to be copied to the correct place: <your_ansible_install_location>/lib/python2.7/site-packages/ansible/plugins/inventory

Alternatively modify your plugin path variable ($ANSIBLE_INVENTORY_PLUGINS) to have it pulled from a custom location.

## Whitelisting
Be default only the host_list, script, auto, yaml, ini, and toml inventory plugins are allowed. To whitelist this plugin, simply add 'ping_addr' in the ansible.cfg here:
<pre><code>
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
</code></pre>
## Generating the inventory
Only a single option is required to generate the inventory, and that's the network in CIDR notation. 

Create a file named ping_addr.yml and add the following contents:
<pre><code>
plugin: ping_addr
network: 10.1.1.0/28
</code></pre>
To see the hosts that would be generated from the inventory plugin, run:
<pre><code>
ansible-inventory -i demo.aws_ec2.yml --graph
</code></pre>

# TODO
* Probably need to add some grouping capability and variables sets. 
* Also need to tweak the ping settings to have a shorter timeout when a host does not respond.
* Need to package it up so that it can be added to an instance easier