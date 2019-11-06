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
import numpy as np
import pyhanabi

global colors
colors = ['R', 'Y', 'G', 'W', 'B']
# ranks = [1,2,3,4,5]
num_in_deck_by_rank = {0:3,1:2,2:2,3:2,4:1} #Note: zero-based


# Note: depending on the object calling, card could either be a dict eg {'color':'R','rank':0} or a HanabiCard instance with c.color() and c.rank() methods
def playable_card(card, fireworks):
  if isinstance(card,pyhanabi.HanabiCard):
    card = {'color':colors[card.color()],'rank':card.rank()}

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

def get_plausible_cards(observation, player_offset, hand_index):
  card_knowledge = observation['pyhanabi'].card_knowledge()[player_offset]
  hidden_card = card_knowledge[hand_index]
  plausible_cards = []
  for color_index in range(5):
    for rank_index in range(5):
      if (hidden_card.color_plausible(color_index) and hidden_card.rank_plausible(rank_index)):
        plausible_card = pyhanabi.HanabiCard(color_index,rank_index)
        plausible_cards.append(plausible_card)
  return plausible_cards


def get_visible_cards(observation,player_offset):
  visible_cards = []
  for other_player in range (1,observation['num_players']):
    if other_player != player_offset:
      their_hand = observation['observed_hands'][other_player]
      for card in their_hand:
        visible_cards.append(card)
  for card in observation['discard_pile']:
    visible_cards.append(card)
  return visible_cards


#This returns an array of the naive probability of each card being playable from a playable from a certain player's perspective
#This ignores conventions, and also doesn't make any inferences based on the information the current player has on their hand

def get_card_playability(observation, player_offset=0):
  visible_cards = get_visible_cards(observation,player_offset)
  # print(observation)
  # print(visible_cards
  my_hand_size = len(observation['observed_hands'][player_offset])
  playability_array = np.zeros(my_hand_size)
  for hand_index in range (my_hand_size):
    total_possibilities = 0
    playable_possibilities = 0
    plausible_cards = get_plausible_cards(observation,player_offset,hand_index)
    for plausible in plausible_cards:
      num_in_deck = num_in_deck_by_rank[plausible.rank()]
      for visible in visible_cards:
        # print(str(plausible) + " " + str(visible))
        # print(visible['color'])
        # print(plausible.color())
        # print(visible['rank'])
        # print(plausible.rank())
        if visible['color'] == colors[plausible.color()] and visible['rank'] == plausible.rank():
          num_in_deck -=1
      total_possibilities += num_in_deck
      if playable_card(plausible,observation['fireworks']):
        playable_possibilities += num_in_deck
    playability_array[hand_index] = playable_possibilities/total_possibilities
    
    # for plausible in plausible_cards:
    #   num_in_deck = num_in_deck_by_rank[plausible.rank()]
    #   possible_in_deck += num_in_deck

    #   for other_player in range (1,observation['num_players']):
    #     if other_player != player_offset
    #       their_hand = observation['observed_hands'][other_player]:
    #         for card in their_hand:
    #           if card['color'] == plausible.color() and card['rank'] == plausible.rank():
    #             possible_in_deck -=1:
      # print(num_in_deck)
      # for player in range(1,observation['num_players']):
      #   if player!= player_offset:



  # print (observation['pyhanabi'].card_knowledge())
  # print(player_hints)
  return playability_array

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
  def play_probably_safe_factory(treshold = 0.95):
    def play_probably_safe_treshold(observation):
      playability_vector = get_card_playability(observation)
      card_index = np.argmax(playability_vector)
      if playability_vector[card_index]>=treshold:
        action = {'action_type': 'PLAY', 'card_index': card_index}
        return action
      return None

    return play_probably_safe_treshold
