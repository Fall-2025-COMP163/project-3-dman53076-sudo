"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Daniel Crandle

AI Usage: Used ChatGPT to help check for errors on my saving and loading functions and had it suggest improvements for data validation. 

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    if character_class not in ["Warrior", "Mage", "Rogue", "Cleric"]:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    stats = base_stats[character_class]

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    return character

def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")
    try:
        with open(filename, 'w') as file:
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")
            file.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            file.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            file.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    except (PermissionError, IOError) as e:
        raise e

def load_character(character_name, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        raise CharacterNotFoundError(f"No save directory found: {save_directory}")
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.isfile(filename):
        raise CharacterNotFoundError(f"Character save file not found: {filename}")
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            character = {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if ":" not in line:
                    raise InvalidSaveDataError(f"Invalid line in save file: {line}")
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]:
                    character[key.lower()] = int(value)
                elif key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                    character[key.lower()] = value.split(",") if value else []
                else:
                    character[key.lower()] = value
            return character
    except IOError:
        raise SaveFileCorruptedError(f"Could not read save file: {filename}")
    except Exception as e:
        raise InvalidSaveDataError(f"Invalid data in save file: {filename}") from e 

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []
    
    character_names = []

    for filename in os.listdir(save_directory):
        suffix = "_save.txt"
        if filename.endswith(suffix):
            character_name = filename[:-len(suffix)]  # Remove '_save.txt'
            character_names.append(character_name)
    return character_names

def delete_character(character_name, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        raise CharacterNotFoundError(f"No save directory found: {save_directory}")
    
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.isfile(filename):
        raise CharacterNotFoundError(f"Character save file not found: {filename}")
    
    try:
        os.remove(filename)
        return True
    except OSError as e:
        raise e

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character['health'] <= 0:
        raise CharacterDeadError(f"Cannot gain experience: {character['name']} is dead")
    level_ups = 0
    character['experience'] += xp_amount
    while character['experience'] >= character['level'] * 100:
        character['experience'] -= character['level'] * 100
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['health'] = character['max_health']
        level_ups += 1
    return level_ups

def add_gold(character, amount):
    if character['gold'] + amount < 0:
        raise ValueError("Gold cannot be negative")
    character['gold'] += amount
    return character['gold']

def heal_character(character, amount):
    character['health'] += amount
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return character['health']

def is_character_dead(character):
    if character['health'] <= 0:
        return True
    else:
        return False

def revive_character(character):
    if character['health'] > 0:
        return False
    character['health'] = character['max_health'] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")
    if not isinstance(character['level'], int) or character['level'] < 1:
        raise InvalidSaveDataError("Invalid level value")
    if not isinstance(character['health'], int) or character['health'] < 0:
        raise InvalidSaveDataError("Invalid health value")
    if not isinstance(character['max_health'], int) or character['max_health'] < 1:
        raise InvalidSaveDataError("Invalid max_health value")
    if not isinstance(character['strength'], int) or character['strength'] < 0: 
        raise InvalidSaveDataError("Invalid strength value")
    if not isinstance(character['magic'], int) or character['magic'] < 0:
        raise InvalidSaveDataError("Invalid magic value")
    if not isinstance(character['experience'], int) or character['experience'] < 0:
        raise InvalidSaveDataError("Invalid experience value")
    if not isinstance(character['gold'], int) or character['gold'] < 0:
        raise InvalidSaveDataError("Invalid gold value")
    if not isinstance(character['inventory'], list):
        raise InvalidSaveDataError("Invalid inventory value")
    if not isinstance(character['active_quests'], list):
        raise InvalidSaveDataError("Invalid active_quests value")
    if not isinstance(character['completed_quests'], list):
        raise InvalidSaveDataError("Invalid completed_quests value")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")

    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")
