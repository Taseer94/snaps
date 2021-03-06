# Copyright (c) 2017 Cable Television Laboratories, Inc. ("CableLabs")
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


class VolumeType:
    """
    SNAPS domain object for Volume Types. Should contain attributes that
    are shared amongst cloud providers
    """
    def __init__(self, name, volume_type_id, public, encryption, qos_spec):
        """
        Constructor
        :param name: the volume's name
        :param volume_type_id: the volume type's id
        :param public: True if public
        :param encryption: instance of a VolumeTypeEncryption domain object
        :param qos_spec: instance of a QoSSpec domain object
        """
        self.name = name
        self.id = volume_type_id
        self.public = public
        self.encryption = encryption
        self.qos_spec = qos_spec

    def __eq__(self, other):
        return (self.name == other.name and self.id == other.id
                and self.public == other.public
                and self.encryption == other.encryption
                and self.qos_spec == other.qos_spec)


class VolumeTypeEncryption:
    """
    SNAPS domain object for Volume Types. Should contain attributes that
    are shared amongst cloud providers
    """
    def __init__(self, volume_encryption_id, volume_type_id,
                 control_location, provider, cipher, key_size):
        """
        Constructor
        :param volume_encryption_id: the encryption id
        :param volume_type_id: the associated volume type's id
        :param control_location: front-end | back-end
        :param provider: the encryption provider class
        :param cipher: the encryption cipher
        :param key_size: the encryption key size
        """
        self.id = volume_encryption_id
        self.volume_type_id = volume_type_id
        self.control_location = control_location
        self.provider = provider
        self.cipher = cipher
        self.key_size = key_size

    def __eq__(self, other):
        return (self.id == other.id
                and self.volume_type_id == other.volume_type_id
                and self.control_location == other.control_location
                and self.provider == other.provider
                and self.cipher == other.cipher
                and self.key_size == other.key_size)


class QoSSpec:
    """
    SNAPS domain object for Volume Types. Should contain attributes that
    are shared amongst cloud providers
    """
    def __init__(self, name, spec_id, consumer):
        """
        Constructor
        :param name: the volume's name
        :param spec_id: the QoS Spec's id
        """
        self.name = name
        self.id = spec_id
        self.consumer = consumer

    def __eq__(self, other):
        return (self.name == other.name and self.id == other.id
                and self.consumer == other.consumer)
