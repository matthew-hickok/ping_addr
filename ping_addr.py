# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
    name: ping_addr
    plugin_type: inventory
    version_added: '2.8'
    author:
      - Matt Hickok
    short_description: Ansible dynamic inventory plugin for Docker swarm nodes.
    requirements:
        - python >= 2.7
    extends_documentation_fragment:
        - constructed
    description: Creates an Ansible inventory based on a ping sweep of the network.
    options:
        plugin:
            description: The name of this plugin, it should always be set to ping_addr for this plugin to
                         recognize it as it's own.
            type: str
            required: true
            choices: ping_addr
        network:
            description: the network in CIDR notation
            type: string
            required: true
'''

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.parsing.utils.addresses import parse_address

import os
import ipaddress


class InventoryModule(BaseInventoryPlugin, Constructable):
    ''' Host inventory parser for ansible using Docker swarm as source. '''

    NAME = 'ping_addr'
    
    def scan_network(self, network):
        network_addresses = list(ipaddress.ip_network(network).hosts())
        VALID_HOSTS = []
        for address in network_addresses:
            response = os.system("ping -c 1 " + str(address) + " > /dev/null 2>&1")
            if response == 0:
                VALID_HOSTS.append(str(address))
        return VALID_HOSTS

    def _fail(self, msg):
        raise AnsibleError(msg)

    def _populate(self):
        raw_params = dict(
            network=self.get_option('network'),
            debug=None,
        )
        online_nodes = self.scan_network(raw_params['network'])
        try:
            self.nodes = online_nodes
            for self.node in self.nodes:
                self.inventory.add_host(self.node)
        except Exception as e:
            raise AnsibleError('holy shit you broke it m8: %s' %
                               to_native(e))

    def verify_file(self, path):
        """Return the possibly of a file being consumable by this plugin."""
        return (
            super(InventoryModule, self).verify_file(path) and
            path.endswith((self.NAME + '.yaml', self.NAME + '.yml')))

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)
        self._populate()
