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


class User:
    """
    SNAPS domain object for Users. Should contain attributes that
    are shared amongst cloud providers
    """
    def __init__(self, name, user_id):
        """
        Constructor
        :param name: the user's name
        :param id: the user's id
        """
        self.name = name
        self.id = user_id

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id
