#  Copyright (c) 2021.  Theo Olausson
#  Copyright (c) 2021.  University of Edinburgh
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met: redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer;
#  redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution;
#  neither the name of the copyright holders nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import glob
import os

from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Backend.SLICC.ModularSLICC.ModularProxy import ModularProxy
from DataObjects.ClassCluster import Cluster
from Debug.Monitor.MakeDir import make_dir
from Backend.SLICC.ModularSLICC.ModularMsg import ModularMsg
from Backend.SLICC.ModularSLICC.ModularDir import ModularDir
from Backend.SLICC.ModularSLICC.ModularCache import ModularCache
from Parser.DataTypes.ClassProtoMachine import ProtoMachine
from Backend.SLICC.ModularSLICC.BackendOptions import GEM5_V20, OPTIONS, BackendOptions
from Backend.SLICC.ModularSLICC.common import Gem5V20


def RunSLICCModular(cluster: Cluster, file_name: str, options: BackendOptions = None) -> None:
    path = os.getcwd()
    # topology-dependent choices of the back end (BackendOptions); defaults otherwise
    for name, value in vars(options or BackendOptions()).items():
        setattr(OPTIONS, name, value)

    make_dir("SLICC")

    (arch,) = cluster.get_global_architectures()

    ModularMsg(arch, file_name)

    directories = cluster.get_machine_architectures_by_type(ProtoMachine.k_dir)
    proxies = [cache for cache in directories if isinstance(cache, HHDirArchitecture)]
    directory, = [dir for dir in directories if not isinstance(dir, HHDirArchitecture)]
    caches = cluster.get_machine_architectures_by_type(ProtoMachine.k_cache)

    machine_ids = {}
    for idx, cntrl in enumerate([*sorted(caches, key=str), *sorted(proxies, key=str)], start=1):
        machine_ids[str(cntrl)] = f"L{idx}Cache"

    machine_ids[str(directory)] = "Directory"
    ModularDir(cluster, directory, file_name, machine_ids)

    for idx, cache in enumerate(sorted(caches, key=str)):
        ModularCache(cluster, cache, file_name, machine_ids, (idx + 1) if len(caches) > 1 else None)

    for idx, proxy in enumerate(sorted(proxies, key=str)):
        ModularProxy(cluster, proxy, file_name, machine_ids, (idx + 1) if len(proxies) > 1 else None)

    if OPTIONS.gem5 == GEM5_V20:
        Gem5V20.rewrite_files(glob.glob(file_name.split(".")[0] + "_*.sm"))

    print("SLICC files were generated in: " + os.getcwd())

    os.chdir(path)
