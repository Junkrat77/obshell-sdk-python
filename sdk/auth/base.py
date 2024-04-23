# coding: utf-8
# Copyright (c) 2024 OceanBase.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from enum import Enum
from typing import List

from model.version import Version


class AuthError(Exception):
    pass


class AuthVersion(Enum):
    V1 = "v1"
    V2 = "v2"


class AuthType(Enum):
    PASSWORD = 1


class OBShellVersion:

    V422 = Version("4.2.2")
    V423 = Version("4.2.3")

    @classmethod
    def __contains__(self, member) -> bool:
        return member in self.__dict__


class Auth:

    def __init__(self, auth_type: str, support_vers: List[Version]) -> None:
        if auth_type not in AuthType.__members__:
            raise ValueError("Invalid auth type")
        self.auth_type = auth_type
        self.support_vers = support_vers
        self._select_version = None
        self._auto_select_version = True
        self.method = None

    def auth(self, request):
        raise NotImplementedError
    
    @property
    def type(self):
        return self.auth_type
    
    def is_support(self, version: Version) -> bool:
        return version in self.support_vers
    
    def set_version(self, version: Version):
        if not self.is_support(version):
            raise ValueError("Version not supported")
        self._select_version = version
        self._auto_select_version = False

    def get_version(self):
        return self._select_version
    
    def auto_select_version(self, vers: List[Version]=[]) -> bool:
        for ver in vers:
            if self.is_support(ver):
                self._select_version = ver
                self._auto_select_version = True
                return True
        return False
    
    def is_auto_select_version(self) -> bool:
        return self._auto_select_version
            
    def reset(self):
        self.method = None

    def reset_method(self):
        if self.method:
            self.method.reset()
    