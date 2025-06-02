#  Copyright (c) 2021.  Nicolai Oswald
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
import itertools
from typing import Union, Dict, List, Set, Tuple
from itertools import product
import os
import random
import time

from Parser.NetworkxParser.ClassProtoParser import ProtoParser

from DataObjects.ClassMachine import Machine
from DataObjects.ClassCluster import Cluster
from DataObjects.ClassLevel import Level

from Algorithms.ControllerGeneration.ProxyDirController.ClassProxyDirArchitecture import ProxyDirArchitecture
from Algorithms.ControllerGeneration.ProxyDirController.ClassHieraCacheArchitecture import HieraCacheArchitecture
from Algorithms.HeteroGen.ClassHHDirArchitecture import HHDirArchitecture
from Algorithms.HeteroGen.ClassHHDirArchitecture_L2private import HHDirArchitecture_L2private
from Algorithms.ProtoAlgoNetworkx.ProtoNetworkxBase import ProtoNetworkxBase

from Algorithms.ControllerGeneration.CompoundBaseController.CompoundDirCacheArchitecture import CompoundDirCacheArchitecture

from MurphiLitmusTests.ClassLitmusTest import LitmusTest
from MurphiLitmusTests.ClassThreadMapLitmusTest import MachThreadMapLitmusTest
from MurphiLitmusTests.ClassLitmusInstruction import LoadInstruction
from Backend.Murphi.RunMurphiModular import RunMurphiCheck, GenerateMurphi, CompileMurphi
from Backend.SLICC.RunSLICCModular import RunSLICCModular

from Debug.Monitor.MakeDir import make_dir, dir_up
from Debug.Monitor.ClassDebug import Debug
from Debug.Monitor.ProtoCCTable import ProtoCCTablePrinter

class RunHH(Debug):

    def __init__(self, default_system_model: bool = False):
        Debug.__init__(self, True)
        self.sys_name = ''
        self.default_system_model = default_system_model

    def run_test(self, filename_1: str, filename_2: str, protocol_dir_path: str,
                 access_map_table: List[Dict[str, List[str]]],
                 litmus_test_list_1: Union[LitmusTest, List[LitmusTest], None] = None,
                 litmus_test_list_2: Union[LitmusTest, List[LitmusTest], None] = None,
                 has_l2_private : bool = False):
        os.chdir(protocol_dir_path)
        protocol_1 = open(filename_1).read()
        protocol_2 = open(filename_2).read()
        self.sys_name = filename_1.split(".")[0] + "_" + filename_2.split(".")[0]
        make_dir("HeteroGen")
        make_dir(self.sys_name)

        # Generate level based on given protocol and check input SSP
        level_1_1 = Level(ProtoParser(protocol_1, filename_1, False, True), "L1")
        level_2_1 = Level(ProtoParser(protocol_2, filename_2, False, True), "L2")
        # level_2_2_1 = Level(ProtoParser(protocol_2, filename_2, False, True), "L2")
        # level_2_2_2 = Level(ProtoParser(protocol_2, filename_2, False, True), "L2")

        # Generate higher level inter cluster protocol

        # For each cluster generate the connecting controllers

        # Generate the proxy caches, which are an input requirement to the HeteroGen controller
        # Proxy Cache interactions with the DIR are atomic, hence generate them before concurrency is generated
        # The new DirProxyCache replaces to original directory architecture in level_1

        # Bridge Generation
        hhgen_ctrl = HHDirArchitecture(level_1_1, level_2_1, access_map_table, False)
        ProtoCCTablePrinter().ptransitiontable(list(level_1_1.directory.get_architecture_transitions()))
        Debug.psection(f"Directory")
        cache_machine_1 = Machine(level_1_1.cache)
        directory_machine_2 = Machine(level_2_1.directory)
        # cache_machine_2 = Machine(level_2.cache)
        hhcache_machine = Machine(level_1_1.directory)
        Debug.psection(f"Cache controller L1")
        ProtoCCTablePrinter().ptransitiontable(list(level_1_1.cache.get_architecture_transitions()))
        Debug.psection(f"Bridge")
        ProtoCCTablePrinter().ptransitiontable(list(level_1_1.directory.get_architecture_transitions()))
        Debug.psection(f"Directory")
        ProtoCCTablePrinter().ptransitiontable(list(level_2_1.directory.get_architecture_transitions()))
                                                                                                                   # L2 private for L1
        if has_l2_private:
            level_1_2_1 = Level(ProtoParser(protocol_1, filename_1, False, True), "L1")
            level_1_2_2 = Level(ProtoParser(protocol_1, filename_1, False, True), "L1")
            l2_private_dir_1 = HHDirArchitecture_L2private(level_1_2_1, level_1_2_2, access_map_table, False)
            Debug.psection(f"Cache controller L1_2 private")
            ProtoCCTablePrinter().ptransitiontable(list(level_1_2_1.directory.get_architecture_transitions()))
            level_1_2_1.directory.global_arch = level_1_1.directory.global_arch
            level_1_2_1.directory.arch_name = "bridge_private"
            l2_private = Machine(level_1_2_1.directory)
            cluster_1 = Cluster(tuple([cache_machine_1, directory_machine_2, hhcache_machine, l2_private]), 'C1', False)
        else:
            cluster_1 = Cluster(
            tuple([cache_machine_1, directory_machine_2, hhcache_machine]),'C1', False)
        RunSLICCModular(cluster_1, self.sys_name)





        # Run ProtoGen for each level
        #ProtoNetworkxBase(level_2)



        # Debug.psection(f"Cache controller L1_2 private")
        # ProtoCCTablePrinter().ptransitiontable(list(level_1_2_1.directory.get_architecture_transitions()))





        #hhcache_machine = Machine(level_2.cache)
        #cache_machine_2 = Machine(hhgen_ctrl.arch_tuple[1])



        # cluster_2 = Cluster( tuple([cache_machine_2, ]) + tuple([hhcache_machine, directory_machine_2]), 'C2', False)

        #cluster_1.update_machine_archs(directory_machine_1.get_arch_list()[0], hhgen_ctrl)
        #cluster_2.update_machine_archs(hhcache_machine_2.get_arch_list()[0], hhgen_ctrl)

        # GenerateMurphi([cluster_1, cluster_2], 'HH_DeadlockFreedom', None)

        #RunMurphiCheck([cluster_1], sys_name, None, 4000, 'DeadlockFreedom')


        #self.verify_flat_protocols(cache_machine_1, cache_machine_2, directory_machine, self.sys_name, 4)

        #cache_thread_dict: Dict[Machine, List[LitmusTest]] = {cache_machine_1: litmus_test_list_1,
        #                                                      cache_machine_2: litmus_test_list_2}

        #if litmus_test_list_1 and litmus_test_list_2:
        #    self.run_litmus_test(self.sys_name, cache_thread_dict, directory_machine)

    def verify_flat_protocols(self,
                              cache_machine_1: Machine, cache_machine_2: Machine, directory_machine: Machine,
                              file_name: str = '', thread_cnt: int = 3):
        make_dir('Deadlock_Tests')
        for cnt_int in range(2, thread_cnt+1):
            deadlock_test_comb = sorted(set([tuple(sorted(comb_tuple, key=lambda x: str(x)))
                                             for comb_tuple in product([cache_machine_1, cache_machine_2],
                                                                       repeat=cnt_int)]),
                                        key=lambda x: str(x))
            for combination in deadlock_test_comb:
                make_dir('_'.join([str(mach).split('_')[-1] for mach in combination]))
                new_cluster = Cluster(combination + tuple([directory_machine]), 'C1', False)
                GenerateMurphi([new_cluster], file_name, None)
                dir_up()

            Debug.psection(f'{self.sys_name} generated {len(deadlock_test_comb)} '
                           f'system combinations for deadlock testing')
        dir_up()

    def run_litmus_test(self, file_name: str, cache_thread_dict: Dict[Machine, List[LitmusTest]],
                        directory_machine: Machine):
        total_tests_generated = 0
        make_dir('Litmus_Tests')  # HACK VARIABLE
        # Get set of litmus test present in all architectures
        cache_thread_set = sorted(self.filter_common_litmus_tests(cache_thread_dict))
        for cache_thread in cache_thread_set:
            make_dir(cache_thread.split('.')[0])

            cache_mach_thread_dict = self.gen_cache_mach_thread_dict(cache_thread, cache_thread_dict)
            perm_list = self.gen_arch_perm_list(cache_mach_thread_dict)
            load_perm_list = self.gen_prefetch_load_permutations(cache_mach_thread_dict, 0)
            for load_perm in load_perm_list:
                for ct_tuple_list in perm_list:
                    self.generate_litmus_test(file_name, ct_tuple_list, load_perm, directory_machine)
                    total_tests_generated += 1
            dir_up()

        Debug.ptext(f'{total_tests_generated} Litmus tests were generated for {file_name} system')

    def generate_litmus_test(self, file_name, ct_tuple_list, load_perm, directory_machine):
        result = '_'.join([str(node[0]).split('_')[-1] for node in ct_tuple_list])
        make_dir(result)
        # Generate the litmus test and the cluster from the permutation
        mach_litmus_test = MachThreadMapLitmusTest(ct_tuple_list[0][1].test_name, ct_tuple_list[0][1].exists)
        mach_list: List[Machine] = []
        for ct_tuple_ind in range(0, len(ct_tuple_list)):
            thread = ct_tuple_list[ct_tuple_ind][1].threads[ct_tuple_ind]. \
                new_prefetch_instructions_thread(load_perm[ct_tuple_ind])
            mach_litmus_test.add_cache_mach_thread_map(ct_tuple_list[ct_tuple_ind][0],
                                                       thread)
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_id_name(ct_tuple_list[ct_tuple_ind], ct_tuple_ind))
            mach_litmus_test.permutation_str_list.append(
                self.gen_thread_prefetch_name(load_perm[ct_tuple_ind]))
            mach_list.append(ct_tuple_list[ct_tuple_ind][0])
        cluster_1 = Cluster(tuple(mach_list) + tuple([directory_machine]), 'C1', False)

        # Update the litmus test name
        litmus_test_thread_perm = '_'.join(mach_litmus_test.permutation_str_list)
        mach_litmus_test.test_name = mach_litmus_test.test_name.split('.')[0] + litmus_test_thread_perm

        GenerateMurphi([cluster_1], file_name, mach_litmus_test)

        dir_up()

    @staticmethod
    def gen_thread_id_name(ct_tuple: Tuple[Machine, LitmusTest], thread_id):
        return ct_tuple[1].memory_consistency_model + str(thread_id)

    @staticmethod
    def gen_thread_prefetch_name(load_perm: Tuple[LoadInstruction]):
        return '_p'+''.join(access.left_assign for access in load_perm)

    @staticmethod
    def filter_common_litmus_tests(cache_thread_dict: Dict[Machine, List[LitmusTest]]) -> Set[str]:
        cache_thread_set = set()
        for cache in cache_thread_dict:
            cache_thread_str_set = set(str(litmus_test) for litmus_test in cache_thread_dict[cache])
            if not cache_thread_set:
                cache_thread_set.update(cache_thread_str_set)
            else:
                cache_thread_set = cache_thread_set.intersection(cache_thread_str_set)
        return cache_thread_set

    @staticmethod
    def gen_cache_mach_thread_dict(cache_thread_type: str, cache_thread_dict: Dict[Machine, List[LitmusTest]]) -> \
            Dict[Machine, LitmusTest]:
        cache_mach_thread_dict: Dict[Machine, LitmusTest] = {}
        for cache in cache_thread_dict:
            for litmus_test in cache_thread_dict[cache]:
                if str(litmus_test) == cache_thread_type:
                    cache_mach_thread_dict[cache] = litmus_test
                    break
        return cache_mach_thread_dict

    @staticmethod
    def gen_arch_perm_list(cache_mach_thread_dict: Dict[Machine, LitmusTest]):
        thread_count = len(list(cache_mach_thread_dict.values())[0].threads)
        perm_elements = list(cache_mach_thread_dict.items())
        perm_list: List[Tuple[Tuple[Machine, LitmusTest], ...]] = \
            [prod for prod in product(perm_elements, repeat=thread_count)]
        return perm_list

    def gen_prefetch_load_permutations(self,
                                       cache_mach_thread_dict: Dict[Machine, LitmusTest], rand_sel_count: int = 0):
        litmus_test = list(cache_mach_thread_dict.values())[0]
        load_permutations = self.gen_simple_prefetch_loads(litmus_test)
        load_permutation_list = [prod for prod in product(load_permutations, repeat=len(litmus_test.threads))]

        if rand_sel_count == -1:
            return load_permutation_list

        sel_load_perm_list = [load_permutation_list[0], load_permutation_list[-1]]
        if rand_sel_count > 0:
            for ind in range(0, 2):
                sel_load_perm_list.append(load_permutation_list[random.randint(1, len(load_permutation_list)-2)])

        return sel_load_perm_list

    @staticmethod
    def gen_simple_prefetch_loads(litmus_test: LitmusTest):
        var_list = list(litmus_test.variable_adr_dict.keys())
        load_instr_list = [LoadInstruction(var, "") for var in var_list]
        load_combinations: List[List[LoadInstruction]] = []
        for ind in range(0, len(load_instr_list)+1):
            load_combinations += itertools.combinations(load_instr_list, ind)
        return load_combinations

