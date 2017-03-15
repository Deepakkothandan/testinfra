# coding: utf-8
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

from __future__ import unicode_literals

import testinfra.backend
import testinfra.modules


class Host(object):
    _host_cache = {}
    _hosts_cache = {}

    def __init__(self, backend):
        self.backend = backend
        self.run = backend.run
        super(Host, self).__init__()

    def __getattr__(self, name):
        assert name in testinfra.modules.modules, name + " is not a module"
        module_class = testinfra.modules.get_module_class(name)
        module = module_class.get_module(self.backend)
        setattr(self, name, module)
        return module

    @classmethod
    def get_host(cls, hostspec, **kwargs):
        key = (hostspec, frozenset(kwargs.items()))
        cache = cls._host_cache
        if key not in cache:
            backend = testinfra.backend.get_backend(hostspec, **kwargs)
            cache[key] = host = cls(backend)
            backend.set_host(host)
        return cache[key]

    @classmethod
    def get_hosts(cls, hosts, **kwargs):
        key = (frozenset(hosts), frozenset(kwargs.items()))
        cache = cls._hosts_cache
        if key not in cache:
            cache[key] = []
            for backend in testinfra.backend.get_backends(hosts, **kwargs):
                host = cls(backend)
                backend.set_host(host)
                cache[key].append(host)
        return cache[key]


get_host = Host.get_host
get_hosts = Host.get_hosts
