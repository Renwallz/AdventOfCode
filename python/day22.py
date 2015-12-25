from collections import namedtuple
from copy import deepcopy
from heapq import heappush, heappop

boss = {'Hit Points': 55, 'Damage': 8}
seen = dict()

class BossDeadException(Exception):
    pass


priority_queue = []
priority_counter = 0  # to prevent issues when two states have the same priority

spell = namedtuple('Spell', ['Name', 'Cost', 'Effect'])
missile = spell('Magic Missile', 53, lambda cs: cs.damage_boss(4))
drain = spell('Drain', 73, lambda cs: cs.damage_boss(2) or cs.heal_player(2))

effect = namedtuple("Effect", ['Name', 'Cost', 'Duration', 'Effect', 'TerminateEffect'])
shield = effect('Shield', 113, 6, lambda cs: cs.set_armor(7), lambda cs: cs.set_armor(0))
poison = effect('Poison', 173, 6, lambda cs: cs.damage_boss(3), None)
recharge = effect('Recharge', 229, 5, lambda cs: cs.gain_mana(101), None)

choices = sorted((missile, drain, shield, poison, recharge), key=lambda x: x.Cost)
min_mana = choices[0].Cost  # the minimum amount of mana you need in order to perform an action


class combat_state(object):
    """Class to store all the details of an existing fight, so they can be restored later"""

    def __init__(self, player_health, player_mana, boss_health, boss_damage, total_mana=0, effects=None):
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
        self.past_choices = None
        self.log = []

    def damage_boss(self, amount):
        self.boss_health -= amount
        if self.boss_health <= 0:
            self.print_choices()
            raise BossDeadException("Boss dead after total mana {}".format(self.total_mana))

    def print_choices(self):
        for line in self.log:
            print(line)

    def heal_player(self, amount):
        self.player_health += amount

    def damage_player(self, amount):
        self.player_health -= amount

    def spend_mana(self, amount):
        self.player_mana -= amount
        self.total_mana += amount

    def gain_mana(self, amount):
        self.player_mana += amount

    def set_armor(self, armor_value):
        self.armor = armor_value

    def add_effect(self, effect):
        if effect.Name in self.effects or effect.Cost > self.player_mana:
            return False
        self.effects[effect.Name] = (effect.Duration, effect)
        self.spend_mana(effect.Cost)
        return True

    def cast_spell(self, spell):
        if spell.Cost > self.player_mana:
            return False
        self.spend_mana(spell.Cost)
        spell.Effect(self)
        return True

    def run_effects(self):
        new_effects = {}
        for effect_name in self.effects:
            duration, effect = self.effects[effect_name]
            self.log.append("{} does it's thing, it's timer is now {}".format(effect_name, duration - 1))
            effect.Effect(self)
            if duration > 1:
                new_effects[effect.Name] = (duration - 1, effect)
            else:
                self.log.append("{} wears off".format(effect_name))
                if effect.TerminateEffect is not None:
                    effect.TerminateEffect(self)

        self.effects = new_effects

    def fight(self):
        stat = self.__repr__()
        if stat in seen:
            if False or self.total_mana >= seen[stat]:
                return False
            seen[stat] = self.total_mana
        seen[stat] = self.total_mana

        if not self.player_turn:
            self.log.append("\n--Boss Turn--")
            self.log.append(
                    "- Player has {} hit points, {} armor, {} mana".format(self.player_health, self.armor,
                                                                           self.player_mana))
            self.log.append("- Boss has {} hit points".format(self.boss_health))

            self.run_effects()

            self.log.append("Boss attacks for {} damage".format(max(self.boss_damage - self.armor, 1)))
            self.damage_player(max(self.boss_damage - self.armor, 1))
            if self.player_health <= 0:
                return False

        self.log.append("\n--Player Turn--")

        self.player_health -= 1
        if self.player_health <= 0:
            return False
        self.log.append(
                "- Player has {} hit points, {} armor, {} mana".format(self.player_health, self.armor,
                                                                       self.player_mana))
        self.log.append("- Boss has {} hit points".format(self.boss_health))

        self.run_effects()

        global priority_queue
        global priority_counter
        if self.player_mana < min_mana:
            return False
        for choice in choices:
            if choice.Cost > self.player_mana:
                break
            new_state = deepcopy(self)
            new_state.log.append("Player casts {}".format(choice.Name))
            if isinstance(choice, spell):
                if not new_state.cast_spell(choice):
                    print(choice.Name)
                    continue
            else:
                if not new_state.add_effect(choice):
                    continue
            new_state.player_turn = False
            priority_counter += 1
            heappush(priority_queue, (new_state.total_mana, priority_counter, new_state))

    def __repr__(self):
        return '|'.join(map(str, [self.player_health, self.player_mana, self.boss_health, hash(str(self.effects))]))


test_start = combat_state(10, 250, 14, 8)
test_start.fight()
print(test_start.log)

while len(priority_queue) > 0:
    total_mana, _, state = heappop(priority_queue)
    try:
        state.fight()
    except BossDeadException as bd:
        print(bd.args)
        priority_queue = []

print('----------------')

seen = dict()
start = combat_state(50, 500, boss['Hit Points'], boss['Damage'], 0)
start.fight()

print(priority_queue)

while len(priority_queue) > 0:
    total_mana, _, state = heappop(priority_queue)
    state.fight()
    # print(total_mana, nsmallest(5, priority_queue))

print("Ran out of options???", priority_queue)
