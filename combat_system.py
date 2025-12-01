"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Daniel Crandle

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    enemy_types = {
        "goblin": {"name": "Goblin", "health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"name": "Orc", "health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"name": "Dragon", "health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100}
    }

    if enemy_type not in enemy_types:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    enemy = enemy_types[enemy_type]
    enemy['max_health'] = enemy['health']
    return enemy

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")  
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
    
# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = False
        self.turn_counter = 0
    
    def start_battle(self):
        if self.character['health'] <= 0:
            raise CharacterDeadError(f"{self.character['name']} is dead and cannot fight!")
        self.combat_active = True
        self.turn_counter = 1
        while self.combat_active:
            self.display_combat_stats(self.character, self.enemy)
            self.player_turn()
            if self.check_battle_end():
                break
            self.enemy_turn()
            if self.check_battle_end():
                break
            self.turn_counter += 1
        if self.enemy['health'] <= 0:
            xp_gained = self.enemy['xp_reward']
            gold_gained = self.enemy['gold_reward']
            return {'winner': 'player', 'xp_gained': xp_gained, 'gold_gained': gold_gained}
        else:
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
    
    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take player turn: combat is not active")
        print("\nYour turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        choice = input("Enter choice (1-3): ")
        if choice == '1':
            calculate_damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, calculate_damage)
            self.display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {calculate_damage} damage!")
        elif choice == '2':
            try:
                ability_result = use_special_ability(self.character, self.enemy)
                self.display_battle_log(ability_result)
            except AbilityOnCooldownError as e:
                self.display_battle_log(str(e))
        elif choice == '3':
            if self.attempt_escape():
                self.display_battle_log(f"{self.character['name']} successfully escaped!")
            else:
                self.display_battle_log(f"{self.character['name']} failed to escape!")
    
    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take enemy turn: combat is not active")
        calculate_damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, calculate_damage)
        self.display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {calculate_damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        damage = attacker['strength'] - (defender['strength'] // 4)
        if damage < 1:
            damage = 1
        return damage
    
    def apply_damage(self, target, damage):
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        if self.enemy['health'] <= 0 or self.character['health'] <= 0:
            self.combat_active = False
            return True
        return False
    
    def attempt_escape(self):
        import random
        random_chance = random.random()
        if random_chance < 0.5:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    if not character.get('ability_ready', True):
        raise AbilityOnCooldownError(f"{character['name']}'s ability is on cooldown!")
    if character['class'] == "Warrior":
        return warrior_power_strike(character, enemy)
    elif character['class'] == "Mage":
        return mage_fireball(character, enemy)
    elif character['class'] == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif character['class'] == "Cleric":
        return cleric_heal(character)
    cooldown = 3  # Example cooldown duration
    character['ability_ready'] = False
    character['ability_cooldown'] = cooldown
    return "Ability used!"

def warrior_power_strike(character, enemy):
    damage = character['strength'] * 2 - (enemy['strength'] // 4)
    if damage < 1:
        damage = 1
    return f"{character['name']} uses Power Strike for {damage} damage!"

def mage_fireball(character, enemy):
    damage = character['magic'] * 2 - (enemy['magic'] // 4)
    if damage < 1:
        damage = 1
    return f"{character['name']} casts Fireball for {damage} damage!"

def rogue_critical_strike(character, enemy):
    import random
    if random.random() < 0.5:
        damage = character['strength'] * 3 - (enemy['strength'] // 4)
        if damage < 1:
            damage = 1
        return f"{character['name']} lands a Critical Strike for {damage} damage!"

def cleric_heal(character):
    heal_amount = 30
    character['health'] += heal_amount
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return f"{character['name']} heals for {heal_amount} health!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    if character['health'] > 0 and not character.get('in_battle', False):
        return True
    return False

def get_victory_rewards(enemy):
    rewards = {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }
    return rewards  

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    try:
        test_char = {
            'name': 'Hero',
            'class': 'Warrior',
            'level': 3,
            'health': 100,
            'max_health': 100,
            'strength': 15,
            'magic': 5,
        }
        goblin = create_enemy("goblin")
        battle = SimpleBattle(test_char, goblin)
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError as e:
        print(f"Cannot start battle: {e}")

