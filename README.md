# KVM Guests Inventory

KVM Guests Inventory is a dynamic Ansible inventory script for KVM guests. It generates an inventory from libvirt dnsmasq status files, allowing easy management of KVM guests through Ansible.

https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html

## Features

- Dynamically generates Ansible inventory from KVM guest information
- Customizable status file location using environment variable
- Easy integration with Ansible playbooks

## Usage

### Basic usage

```bash
$ ./kvm-guests-inventory.py --list
```

This will list all KVM guests using the default status file (/var/lib/libvirt/dnsmasq/virbr0.status).

### Use a custom status file

```bash
$ KVM_GUESTS_STATUS_FILE=/path/to/custom/status/file ./kvm-guests-inventory.py --list
```

### Get variables for a specific host

```bash
$ ./kvm-guests-inventory.py --host hostname
```

## Integration with Ansible

To use this inventory script with Ansible, you can specify it as the inventory source in your ansible-playbook command:

```bash
$ ansible-playbook -i ./kvm-guests-inventory.py your_playbook.yml
```

### Examples

1. Use a custom status file:

```bash
$ KVM_GUESTS_STATUS_FILE=/path/to/custom/status/file ansible-playbook -i ./kvm-guests-inventory.py your_playbook.yml
```

2. Target only the KVM guests group:

```bash
$ ansible-playbook -i ./kvm-guests-inventory.py -l vm_name your_playbook.yml
```

## Environment Variables

- `KVM_GUESTS_STATUS_FILE`: Path to the dnsmasq status file. If not set, defaults to '/var/lib/libvirt/dnsmasq/virbr0.status'.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) for details.
