# Tapisctl 

Based on Ansible playbooks and roles. Used for generating deployment files for tapis. 

Includes both Docker and Kubernetes deployment flavors.

## Install

Run as regular user (e.g. rocky).

Install Ansible using your Linux distro package manager. e.g. For Rocky Linux:

    # sudo dnf install ansible libselinux-python3

Install Ansible community module:

    # ansible-galaxy collection install community.general

For testing you can use one of the inventory_example inventories. For example

    # ansible-playbook -i inventory_example/docker-inventory.yml playbooks/generate.yml

After running you should find ~/tmp/tapisquickstart-docker1 containing docker compose.yml files for each Tapis component.

There is a similar example playbook for Kubernetes inventory_example/kube-inventory.yml.

## Customize Your Install

Copy the inventory_example dir out of the repo dir and start modifying the hosts and host_vars files to suit your needs. 

    # cp -r inventory_example ~/inventory
    # mv ~/inventory/docker-inventory.yml ~/inventory/hosts

For example if you want to change the location of the generated files, add a var to the ~/inventory/hosts file:

    tapis_installs:
      hosts:
        tapisquickstart-docker1:
          ansible_connection: local
          tapisflavor: docker
          tapisdir: '{{ ansible_env.HOME }}/tmp/tapis-1.3'

(See Ansible docs for more setup.)

Run the playbook after making changes:

    # ansible-playbook -i ~/inventory/hosts playbooks/generate.yml

## Docker vs. Kubernetes Installation

You can generate either Docker- or Kubernetes-specific deployment files using the same playbooks. You specify this in your inventory (hosts file) by specifying the `tapisflavor` variable one of 2 ways.

      tapisflavor: docker

or:

      tapisflavor: kube


## Other Playbooks

There are several other playbooks to help with other things, for example for printing all the config variables:

    # ansible-playbook -i ~/inventory/hosts playbooks/showconf.yml

