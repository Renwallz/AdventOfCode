from collections import namedtuple
from copy import deepcopy
from heapq import heappush

boss = {'Hit Points': 55, 'Damage': 8}


class BossDeadException(Exception):
    pass


priority_queue = []
priority_counter = 0  # to prevent issues when two states have the same priority

spell = namedtuple('Spell', ['Name', 'Cost', 'Effect'])
missile = spell('Magic Missile', 53, lambda cs: cs.alter_boss_health(-4))
drain = spell('Drain', 73, lambda cs: cs.alter_boss_health(-2) and cs.alter_player_health(2))

effect = namedtuple("Effect", ['Name', 'Cost', 'Duration', 'Effect', 'TerminateEffect'])
shield = effect('Shield', 113, 6, lambda cs: cs.set_armor(7), lambda cs: cs.set_armor(0))
poison = effect('Poison', 173, 6, lambda cs: cs.alter_boss_health(-3), None)
recharge = effect('Recharge', 229, 5, lambda cs: cs.alter_player_mana(101), None)

choices = (missile, drain, shield, poison, recharge)
min_mana = choices[0].Cost  # the minimum amount of mana you need in order to perform an action


class combat_state(object):
    """Class to store all the details of an existing fight, so they can be restored later"""

    def __init__(self, player_health, player_mana, boss_health, boss_damage, total_mana, effects=None):
        self.player_health = player_health
        self.player_mana = player_mana
        self.boss_health = boss_health
        self.boss_damage = boss_damage
        self.total_mana = total_mana
        if effects is None:
            self.effects = {}
        else:
            self.effects = effects

        self.player_turn = True
        self.armor = 0

    def alter_boss_health(self, change):
        self.boss_health += change
        if self.boss_health <= 0:
            raise BossDeadException("Boss dead after total mana {}".format(self.total_mana))

    def alter_player_health(self, change):
        self.player_health += change

    def alter_player_mana(self, change):
        self.player_mana += change
        if change < 0:
            self.total_mana += (change * -1)

    def set_armor(self, armor_value):
        self.armor = armor_value

    def add_effect(self, effect):
        if effect.Name in self.effects or effect.Cost > self.player_mana:
            return False
        self.effects[effect.Name] = (effect.Duration, effect)
        self.alter_player_mana(effect.Cost * -1)

    def cast_spell(self, spell):
        if spell.Cost > self.player_mana:
            return False
        spell.Effect(self)
        self.alter_player_mana(spell.Cost * -1)

    def run_effects(self):
        new_effects = {}
        for effect_name in self.effects:
            duration, effect = self.effects[effect_name]
            if duration > 0:
                effect.Effect(self)
                new_effects[effect.Name] = (duration - 1, effect)
            else:
                if effect.TerminateEffect is not None:
                    effect.TerminateEffect(self)

        self.effects = new_effects

    def fight(self):
        self.run_effects()

        if self.player_turn:
            global priority_queue
            global priority_counter
            if self.player_mana < min_mana:
                return False
            for choice in choices:
                if choice.Cost > self.player_mana:
                    break
                new_state = deepcopy(self)
                if isinstance(choice, spell):
                    new_state.cast_spell(choice)
                else:
                    new_state.add_effect(choice)
                priority_counter += 1
                heappush(priority_queue, (new_state.total_mana, priority_counter, new_state))

        else:
            self.alter_player_health(max(self.boss_damage - self.armor, 1))
            if self.player_health <= 0:
                return False

        self.player_turn = not self.player_turn

    def __repr__(self):
        return '|'.join(map(str, [self.player_mana, self.player_health, self.boss_health, self.total_mana]))


start = combat_state(50, 500, boss['Hit Points'], boss['Damage'], 0)
start.fight()

print(priority_queue)

'''while len(priority_queue) > 0:
    total_mana, _, state = heappop(priority_queue)
    state.fight()'''
