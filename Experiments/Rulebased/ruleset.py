# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Simple Agent."""

from rl_env import Agent
import random

class Ruleset():
  

  @staticmethod
  def legal_random(observation):
    """Act based on an observation."""
    if observation['current_player_offset'] == 0:
      action = random.choice(observation['legal_moves'])
      return action
    else:
      return None

  @staticmethod
  def discard_randomly(observation):
    if observation['information_tokens'] < 8:
      player_offset = 0
      hand = observation['observed_hands'][player_offset]
      hand_size = len(hand)
      discard_index = random.randint(0,hand_size-1)
      return {'action_type': 'DISCARD', 'card_index': discard_index}
    return None