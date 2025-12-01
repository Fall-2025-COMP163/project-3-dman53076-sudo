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
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
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
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        pass
    
    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take enemy turn: combat is not active")
        calculate_damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, calculate_damage)
        self.display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {calculate_damage} damage!")
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
    
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
        random_chance = random.random(1, 100)
        if random_chance < 50:
            self.combat_active = False
            return True
        return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    pass

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    if character['health'] > 0 and not character.get('in_battle', False):
        return True

def get_victory_rewards(enemy):
    rewards = {
        'xp': enemy['xp_reward'],
        'gold': enemy['gold_reward']
    }
    return rewards  

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

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
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

