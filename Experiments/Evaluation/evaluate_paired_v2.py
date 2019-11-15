# coding=utf-8
# Copyright 2018 The Dopamine Authors and Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
# This file is a fork of the original Dopamine code incorporating changes for
# the multiplayer setting and the Hanabi Learning Environment.
#
"""The entry point for running a Rainbow agent on Hanabi."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
import statistics
import pandas as pd

import rl_env
from third_party.dopamine import logger
from third_party.dopamine import checkpointer
from internal_agent import InternalAgent
from agents.random_agent import RandomAgent
from agents.simple_agent import SimpleAgent
from internal_agent import InternalAgent
from rulebased_agent import RulebasedAgent
from outer_agent import OuterAgent
import run_paired_experiment

AGENT_CLASSES = {'SimpleAgent': SimpleAgent, 'RandomAgent': RandomAgent, 'InternalAgent': InternalAgent,'OuterAgent':OuterAgent, 'RainbowAgent':None}
SETTINGS = {'players': 2, 'num_episodes': 10, 'agent_class1': 'SimpleAgent', 'agent_class2': 'RandomAgent'}

FLAGS = flags.FLAGS
environment = rl_env.make()
observations = environment.reset()
print(observations['legal_moves'])
"""
observations = self.enviroment.reset() 1?2?
reward 1?2?
?.step(self, reward, current_player, legal_actions, observation)
agent1 =?
action = ?._select_action
"""
