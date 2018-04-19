#!/usr/bin/python
#
# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Show bcache-devices.

This script will loop through all the block devices on a node and return all the
bcache devices along with whether they are caching or backing.
"""                 

import sys
from subprocess import check_output,Popen,PIPE

sys.path.append('hooks')
from charmhelpers.core.hookenv import log, action_set

def enumerate_disks():          
        disks = check_output("lsblk -l | tail -n +2 | awk '{print $1}'",shell=True).split()
        Caches = []
        bcaches = {}
        for i in disks:
                cmd = "bcache-super-show /dev/" + i + " | grep sb.version"
                check = Popen(cmd, shell=True,stdout=PIPE,stderr=PIPE)
                cache_check = check.communicate()[0].split()
                if cache_check and 'cache' in cache_check[2]:
                    Caches.append(i)
                elif cache_check and 'backing' in cache_check[2]:
                        cmd2 = "lsblk -l /dev/" + i + " | tail -n +3 | awk '{print $1}'"
                        b_name = check_output(cmd2, shell = True).rstrip()
                        bcaches[b_name] = i
        return Caches, bcaches

def get_bcaches(cache_disk,backing_disks):
    result = {}
    for i in cache_disk:
        cmd = "lsblk -l /dev/" + i + " | tail -n +3 | awk '{print $1}'"
        b_caches = check_output(cmd, shell = True).split()
        disks = []
        for b in b_caches:
                backing_disks[b] = backing_disks[b] + (get_state(backing_disks[b])).rstrip()
                disks.append(backing_disks[b])
        action_set({ i : ' '.join(disks)})


def get_state(disk):
        cmd = "sudo bcache-super-show /dev/" + disk + " | grep state | awk '{print $3}'"
        disk_state = check_output(cmd, shell=True)
        return disk_state

if __name__ == '__main__':
        caches, bcaches = enumerate_disks()
        get_bcaches(caches,bcaches)
