#!/usr/bin/env python3

"""
kvm-guests-inventory - Dynamic Ansible inventory for KVM guests

This script generates a dynamic Ansible inventory from libvirt dnsmasq status files.
The status file location can be specified using the KVM_GUESTS_STATUS_FILE environment variable.

Usage:
  KVM_GUESTS_STATUS_FILE=/path/to/status/file ./kvm-guests-inventory.py --list
  KVM_GUESTS_STATUS_FILE=/path/to/status/file ./kvm-guests-inventory.py --host <hostname>
"""

import argparse
import json
import sys
import os

DEFAULT_STATUS_FILE = '/var/lib/libvirt/dnsmasq/virbr0.status'

class KVMGuestsInventory:
    def __init__(self, status_file):
        self.status_file = status_file
        self.inventory = {
            '_meta': {
                'hostvars': {}
            },
            'all': {
                'hosts': [],
                'children': ['kvm_guests']
            },
            'kvm_guests': {
                'hosts': []
            }
        }

    def read_status_file(self):
        try:
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Status file {self.status_file} not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in status file {self.status_file}.", file=sys.stderr)
            sys.exit(1)

    def generate_inventory(self):
        status_data = self.read_status_file()

        for host in status_data:
            hostname = host['hostname']
            self.inventory['all']['hosts'].append(hostname)
            self.inventory['kvm_guests']['hosts'].append(hostname)
            self.inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': host['ip-address'],
                'mac_address': host['mac-address'],
                'client_id': host['client-id'],
                'expiry_time': host['expiry-time']
            }

    def get_inventory(self):
        return self.inventory

    def get_host_vars(self, hostname):
        return self.inventory['_meta']['hostvars'].get(hostname, {})

def main():
    parser = argparse.ArgumentParser(description='KVM Guests Inventory for Ansible')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='List all hosts')
    group.add_argument('--host', help='Get variables for a specific host')
    args = parser.parse_args()

    status_file = os.environ.get('KVM_GUESTS_STATUS_FILE', DEFAULT_STATUS_FILE)

    inventory = KVMGuestsInventory(status_file)
    inventory.generate_inventory()

    if args.list:
        print(json.dumps(inventory.get_inventory(), indent=2))
    elif args.host:
        print(json.dumps(inventory.get_host_vars(args.host), indent=2))

if __name__ == '__main__':
    main()
