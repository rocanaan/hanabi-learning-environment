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

global colors
colors = ['Y', 'B', 'W', 'R', 'G']


def playable_card(card, fireworks):
  """A card is playable if it can be placed on the fireworks pile."""
  if card['color'] == None and card['rank'] != None:
      for color in colors:
          if fireworks[color] == card['rank']:
              continue
          else:
              return False

      return True
  elif card['color'] == None or card['rank'] == None:
      return False
  else:
      return card['rank'] == fireworks[card['color']]
  

class Ruleset():


  @staticmethod
  def play_safe_card(observation):
    fireworks = observation['fireworks']
    for card_index, hint in enumerate(observation['card_knowledge'][0]):
      if playable_card(hint, fireworks):
          return {'action_type': 'PLAY', 'card_index': card_index}
    return None


  @staticmethod
  def tell_playable_card_outer(observation):
    fireworks = observation['fireworks']

    # Check if it's possible to hint a card to your colleagues.
    if observation['information_tokens'] > 0:
      # Check if there are any playable cards in the hands of the opponents.
      for player_offset in range(1, observation['num_players']):
        player_hand = observation['observed_hands'][player_offset]
        player_hints = observation['card_knowledge'][player_offset]
        # Check if the card in the hand of the opponent is playable.
        for card, hint in zip(player_hand, player_hints):
          if playable_card(card,fireworks) and hint['color'] is None:
            return {
             'action_type': 'REVEAL_COLOR',
             'color': card['color'],
             'target_offset': player_offset
            }
          elif playable_card(card, fireworks) and hint['rank'] is None:
            return {
             'action_type': 'REVEAL_RANK',
             'rank': card['rank'],
             'target_offset': player_offset
            }
    return None


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

    @staticmethod
    def play_probably_safe_factory(treshold = 1.0):
      def play_probably_safe_treshold(observation):
        return observation, treshold

      return play_probably_safe_treshold
