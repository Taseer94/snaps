# Copyright (c) 2016 Cable Television Laboratories, Inc. ("CableLabs")
#                    and others.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import logging
import keystone_utils

from novaclient.client import Client
from novaclient.exceptions import NotFound

__author__ = 'spisarski'

logger = logging.getLogger('nova_utils')

"""
Utilities for basic OpenStack Nova API calls
"""


def nova_client(os_creds):
    """
    Instantiates and returns a client for communications with OpenStack's Nova server
    :param os_creds: The connection credentials to the OpenStack API
    :return: the client object
    """
    logger.debug('Retrieving Nova Client')
    return Client(os_creds.compute_api_version, session=keystone_utils.keystone_session(os_creds))


def get_servers_by_name(nova, name):
    """
    Returns a list of servers with a given name
    :param nova: the Nova client
    :param name: the server name
    :return: the list of servers
    """
    return nova.servers.list(search_opts={'name': name})


def get_latest_server_object(nova, server):
    """
    Returns a server with a given id
    :param nova: the Nova client
    :param server: the old server object
    :return: the list of servers or None if not found
    """
    return nova.servers.get(server)


def save_keys_to_files(keys=None, pub_file_path=None, priv_file_path=None):
    """
    Saves the generated RSA generated keys to the filesystem
    :param keys: the keys to save
    :param pub_file_path: the path to the public keys
    :param priv_file_path: the path to the private keys
    :return: None
    """
    if keys:
        if pub_file_path:
            pub_dir = os.path.dirname(pub_file_path)
            if not os.path.isdir(pub_dir):
                os.mkdir(pub_dir)
            public_handle = open(pub_file_path, 'wb')
            public_handle.write(keys.publickey().exportKey('OpenSSH'))
            public_handle.close()
            os.chmod(pub_file_path, 0o400)
            logger.info("Saved public key to - " + pub_file_path)
        if priv_file_path:
            priv_dir = os.path.dirname(priv_file_path)
            if not os.path.isdir(priv_dir):
                os.mkdir(priv_dir)
            private_handle = open(priv_file_path, 'wb')
            private_handle.write(keys.exportKey())
            private_handle.close()
            os.chmod(priv_file_path, 0o400)
            logger.info("Saved private key to - " + priv_file_path)


def upload_keypair_file(nova, name, file_path):
    """
    Uploads a public key from a file
    :param nova: the Nova client
    :param name: the keypair name
    :param file_path: the path to the public key file
    :return: the keypair object
    """
    with open(os.path.expanduser(file_path)) as fpubkey:
        logger.info('Saving keypair to - ' + file_path)
        return upload_keypair(nova, name, fpubkey.read())


def upload_keypair(nova, name, key):
    """
    Uploads a public key from a file
    :param nova: the Nova client
    :param name: the keypair name
    :param key: the public key object
    :return: the keypair object
    """
    logger.info('Creating keypair with name - ' + name)
    return nova.keypairs.create(name=name, public_key=key)


def keypair_exists(nova, keypair_obj):
    """
    Returns a copy of the keypair object if found
    :param nova: the Nova client
    :param keypair_obj: the keypair object
    :return: the keypair object or None if not found
    """
    try:
        return nova.keypairs.get(keypair_obj)
    except:
        return None


def get_keypair_by_name(nova, name):
    """
    Returns a list of all available keypairs
    :param nova: the Nova client
    :param name: the name of the keypair to lookup
    :return: the keypair object or None if not found
    """
    keypairs = nova.keypairs.list()

    for keypair in keypairs:
        if keypair.name == name:
            return keypair

    return None


def delete_keypair(nova, key):
    """
    Deletes a keypair object from OpenStack
    :param nova: the Nova client
    :param key: the keypair object to delete
    """
    logger.debug('Deleting keypair - ' + key.name)
    nova.keypairs.delete(key)


def get_floating_ip_pools(nova):
    """
    Returns all of the available floating IP pools
    :param nova: the Nova client
    :return: a list of pools
    """
    return nova.floating_ip_pools.list()


def get_floating_ips(nova):
    """
    Returns all of the floating IPs
    :param nova: the Nova client
    :return: a list of floating IPs
    """
    return nova.floating_ips.list()


def create_floating_ip(nova, ext_net_name):
    """
    Returns the floating IP object that was created with this call
    :param nova: the Nova client
    :param ext_net_name: the name of the external network on which to apply the floating IP address
    :return: the floating IP object
    """
    logger.info('Creating floating ip to external network - ' + ext_net_name)
    return nova.floating_ips.create(ext_net_name)


def get_floating_ip(nova, floating_ip):
    """
    Returns a floating IP object that should be identical to the floating_ip parameter
    :param nova: the Nova client
    :param floating_ip: the floating IP object to lookup
    :return: hopefully the same floating IP object input
    """
    logger.debug('Attempting to retrieve existing floating ip with IP - ' + floating_ip.ip)
    return nova.floating_ips.get(floating_ip)


def delete_floating_ip(nova, floating_ip):
    """
    Responsible for deleting a floating IP
    :param nova: the Nova client
    :param floating_ip: the floating IP object to delete
    :return:
    """
    logger.debug('Attempting to delete existing floating ip with IP - ' + floating_ip.ip)
    return nova.floating_ips.delete(floating_ip)


def get_nova_availability_zones(nova):
    """
    Returns the names of all nova compute servers
    :param nova: the Nova client
    :return: a list of compute server names
    """
    out = list()
    zones = nova.availability_zones.list()
    for zone in zones:
        if zone.zoneName == 'nova':
            for key, host in zone.hosts.iteritems():
                out.append(zone.zoneName + ':' + key)

    return out


def delete_vm_instance(nova, vm_inst):
    """
    Deletes a VM instance
    :param nova: the nova client
    :param vm_inst: the OpenStack instance object to delete
    """
    nova.servers.delete(vm_inst)


def get_flavor_by_name(nova, name):
    """
    Returns a flavor by name
    :param nova: the Nova client
    :param name: the flavor name to return
    :return: the OpenStack flavor object or None if not exists
    """
    try:
        return nova.flavors.find(name=name)
    except NotFound:
        return None


def create_flavor(nova, flavor_settings):
    """
    Creates and returns and OpenStack flavor object
    :param nova: the Nova client
    :param flavor_settings: the flavor settings
    :return: the Flavor
    """
    return nova.flavors.create(name=flavor_settings.name, flavorid=flavor_settings.flavor_id, ram=flavor_settings.ram,
                               vcpus=flavor_settings.vcpus, disk=flavor_settings.disk,
                               ephemeral=flavor_settings.ephemeral, swap=flavor_settings.swap,
                               rxtx_factor=flavor_settings.rxtx_factor, is_public=flavor_settings.is_public)


def delete_flavor(nova, flavor):
    """
    Deletes a flavor
    :param nova: the Nova client
    :param flavor: the OpenStack flavor object
    """
    nova.flavors.delete(flavor)


def add_security_group(nova, vm, security_group_name):
    """
    Adds a security group to an existing VM
    :param nova: the nova client
    :param vm: the OpenStack server object (VM) to alter
    :param security_group_name: the name of the security group to add
    """
    nova.servers.add_security_group(str(vm.id), security_group_name)


def remove_security_group(nova, vm, security_group):
    """
    Removes a security group from an existing VM
    :param nova: the nova client
    :param vm: the OpenStack server object (VM) to alter
    :param security_group: the OpenStack security group object to add
    """
    nova.servers.remove_security_group(str(vm.id), security_group['security_group']['name'])
