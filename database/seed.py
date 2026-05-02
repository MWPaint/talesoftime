"""
seed.py - Populates all reference / lookup tables with initial data.
Run once: python database/seed.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import get_db, init_db

LOOKUP_SEED_DATA = {
    "CharacterClass": [
        {"ClassName": "Warrior",  "Description": "A powerful melee fighter."},
        {"ClassName": "Mage", "Description": "A powerful ranged spell caster."},
        {"ClassName": "Paladin", "Description": "A tanky melee fighter for the frontlines."},
        {"ClassName": "Priest", "Description": "A ranged spell caster excelling in healing spells."},
        {"ClassName": "Rogue", "Description": "A stealthy melee fighter."},
        {"ClassName": "Archer", "Description": "A powerful ranged fighter."},
    ],
    "Species": [
        {"SpeciesName": "Human"},
        {"SpeciesName": "Elf"},
        {"SpeciesName": "Dwarf"},
        {"SpeciesName": "Dragonborn"},
        {"SpeciesName": "Orc"},
        {"SpeciesName": "Demon"},
    ],
    "Alignment": [
        {"AlignmentName": "Lawful Good"},
        {"AlignmentName": "Chaotic Good"},
        {"AlignmentName": "Neutral Good"},
        {"AlignmentName": "Lawful Evil"},
        {"AlignmentName": "Chaotic Evil"},
        {"AlignmentName": "Neutral Evil"},
    ],
    "ItemType": [
        {"TypeName": "Weapon"},
        {"TypeName": "Potion"},
        {"TypeName": "Gold"},
        {"TypeName": "Herb"},
        {"TypeName": "Armour"},
        {"TypeName": "Clothing"},
    ],
    "Rarity": [
        {"RarityName": "Common"},
        {"RarityName": "Uncommon"},
        {"RarityName": "Rare"},
        {"RarityName": "Epic"},
        {"RarityName": "Legendary"},
        {"RarityName": "Mythic"},
    ],
    "Region": [
        {"RegionName": "The Verdant Vale"},
        {"RegionName": "Distant Roost"},
        {"RegionName": "Wetland Aspect"},
        {"RegionName": "Scorched Acres"},
        {"RegionName": "Abyssal Depths"},
        {"RegionName": "Sky Meadow"},
    ],
    "Difficulty": [
        {"DifficultyName": "Novice"},
        {"DifficultyName": "Apprentice"},
        {"DifficultyName": "Journeyman"},
        {"DifficultyName": "Expert"},
        {"DifficultyName": "Master"},
        {"DifficultyName": "Legendary"},
    ],
}


def table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) AS Total FROM {table_name}")
    return cursor.fetchone()["Total"]


def fetch_lookup_map(cursor, table_name, key_field):
    cursor.execute(f"SELECT * FROM {table_name}")
    return {row[key_field]: dict(row) for row in cursor.fetchall()}


def seed_lookup_tables(cursor):
    for table_name, rows in LOOKUP_SEED_DATA.items():
        if table_count(cursor, table_name) == 0:
            for row in rows:
                columns      = ", ".join(row.keys())
                placeholders = ", ".join(["?"] * len(row))
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                    tuple(row.values())
                )
            print(f"  ✔ Seeded {table_name}")
        else:
            print(f"  – Skipped {table_name} (already has data)")


def seed_core_data(cursor):
    if table_count(cursor, "Character") > 0:
        print("  – Skipped Character / Item / Quest / Inventory / CharacterQuest (already has data)")
        return

    classes    = fetch_lookup_map(cursor, "CharacterClass", "ClassName")
    species    = fetch_lookup_map(cursor, "Species",        "SpeciesName")
    alignments = fetch_lookup_map(cursor, "Alignment",      "AlignmentName")
    item_types = fetch_lookup_map(cursor, "ItemType",       "TypeName")
    rarities   = fetch_lookup_map(cursor, "Rarity",         "RarityName")
    regions    = fetch_lookup_map(cursor, "Region",         "RegionName")
    difficulties = fetch_lookup_map(cursor, "Difficulty",   "DifficultyName")

    # ── Characters ────────────────────────────────────────────────────────────
    character_rows = [
        {"CharacterName": "Thorin Ironblade",    "ClassID": classes["Warrior"]["ClassID"],  "SpeciesID": species["Dwarf"]["SpeciesID"],  "AlignmentID": alignments["Lawful Good"]["AlignmentID"],     "Level": 12},
        {"CharacterName": "Pan Yinhu",    "ClassID": classes["Paladin"]["ClassID"],  "SpeciesID": species["Orc"]["SpeciesID"],  "AlignmentID": alignments["Chaotic Good"]["AlignmentID"],     "Level": 5},
        {"CharacterName": "Astra Yao",    "ClassID": classes["Archer"]["ClassID"],  "SpeciesID": species["Elf"]["SpeciesID"],  "AlignmentID": alignments["Neutral Good"]["AlignmentID"],     "Level": 13},
        {"CharacterName": "Von Lycaon",    "ClassID": classes["Rogue"]["ClassID"],  "SpeciesID": species["Demon"]["SpeciesID"],  "AlignmentID": alignments["Chaotic Evil"]["AlignmentID"],     "Level": 9},
        {"CharacterName": "Hoshimi Miyabi",    "ClassID": classes["Mage"]["ClassID"],  "SpeciesID": species["Dragonborn"]["SpeciesID"],  "AlignmentID": alignments["Lawful Evil"]["AlignmentID"],     "Level": 15},
        {"CharacterName": "Lucia Elowen",    "ClassID": classes["Priest"]["ClassID"],  "SpeciesID": species["Dwarf"]["SpeciesID"],  "AlignmentID": alignments["Neutral Evil"]["AlignmentID"],     "Level": 20},
    ]

    for row in character_rows:
        cursor.execute("""
            INSERT INTO Character (CharacterName, ClassID, SpeciesID, AlignmentID, Level)
            VALUES (?, ?, ?, ?, ?)
        """, (row["CharacterName"], row["ClassID"], row["SpeciesID"], row["AlignmentID"], row["Level"]))

    print("  ✔ Seeded Character")
    character_map = fetch_lookup_map(cursor, "Character", "CharacterName")

    # ── Items ─────────────────────────────────────────────────────────────────
    item_rows = [
        {"ItemName": "Iron Sword",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Common"]["RarityID"]},
        {"ItemName": "Steel Shield",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Uncommon"]["RarityID"]},
        {"ItemName": "Diamond Bow",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Rare"]["RarityID"]},
        {"ItemName": "Ruby Dagger",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Epic"]["RarityID"]},
        {"ItemName": "Sapphire Wand",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Legendary"]["RarityID"]},
        {"ItemName": "Amethyst Staff",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Mythic"]["RarityID"]},
    ]

    for row in item_rows:
        cursor.execute("""
            INSERT INTO Item (ItemName, ItemTypeID, RarityID)
            VALUES (?, ?, ?)
        """, (row["ItemName"], row["ItemTypeID"], row["RarityID"]))

    print("  ✔ Seeded Item")
    item_map = fetch_lookup_map(cursor, "Item", "ItemName")

    # ── Quests ────────────────────────────────────────────────────────────────
    quest_rows = [
        {"QuestName": "Defend the Vale",       "RegionID": regions["The Verdant Vale"]["RegionID"],        "DifficultyID": difficulties["Journeyman"]["DifficultyID"]},
        {"QuestName": "Escort the villagers",       "RegionID": regions["Distant Roost"]["RegionID"],        "DifficultyID": difficulties["Novice"]["DifficultyID"]},
        {"QuestName": "Collect medicinal herbs",       "RegionID": regions["Wetland Aspect"]["RegionID"],        "DifficultyID": difficulties["Apprentice"]["DifficultyID"]},
        {"QuestName": "Defeat Mythrix",       "RegionID": regions["Sky Meadow"]["RegionID"],        "DifficultyID": difficulties["Expert"]["DifficultyID"]},
        {"QuestName": "Slay 15 Mimics",       "RegionID": regions["Scorched Acres"]["RegionID"],        "DifficultyID": difficulties["Master"]["DifficultyID"]},
        {"QuestName": "Repair the castle wall",       "RegionID": regions["Abyssal Depths"]["RegionID"],        "DifficultyID": difficulties["Legendary"]["DifficultyID"]},
    ]

    for row in quest_rows:
        cursor.execute("""
            INSERT INTO Quest (QuestName, RegionID, DifficultyID)
            VALUES (?, ?, ?)
        """, (row["QuestName"], row["RegionID"], row["DifficultyID"]))

    print("  ✔ Seeded Quest")
    quest_map = fetch_lookup_map(cursor, "Quest", "QuestName")

    # ── Inventory ─────────────────────────────────────────────────────────────
    inventory_rows = [
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "ItemID": item_map["Iron Sword"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Pan Yinhu"]["CharacterID"],    "ItemID": item_map["Steel Shield"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Astra Yao"]["CharacterID"],    "ItemID": item_map["Diamond Bow"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Von Lycaon"]["CharacterID"],    "ItemID": item_map["Ruby Dagger"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Hoshimi Miyabi"]["CharacterID"],    "ItemID": item_map["Sapphire Wand"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Lucia Elowen"]["CharacterID"],    "ItemID": item_map["Amethyst Staff"]["ItemID"],           "Quantity": 1},
    ]

    for row in inventory_rows:
        cursor.execute("""
            INSERT INTO Inventory (CharacterID, ItemID, Quantity)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["ItemID"], row["Quantity"]))

    print("  ✔ Seeded Inventory")

    # ── CharacterQuest ────────────────────────────────────────────────────────
    character_quest_rows = [
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "QuestID": quest_map["Defend the Vale"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Pan Yinhu"]["CharacterID"],    "QuestID": quest_map["Escort the villagers"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Astra Yao"]["CharacterID"],    "QuestID": quest_map["Collect medicinal herbs"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Von Lycaon"]["CharacterID"],    "QuestID": quest_map["Defeat Mythrix"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Hoshimi Miyabi"]["CharacterID"],    "QuestID": quest_map["Slay 15 Mimics"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Lucia Elowen"]["CharacterID"],    "QuestID": quest_map["Repair the castle wall"]["QuestID"],       "CompletionDate": datetime(2026, 1, 12, 14, 30).isoformat(sep=" ")},
    ]

    for row in character_quest_rows:
        cursor.execute("""
            INSERT INTO CharacterQuest (CharacterID, QuestID, CompletionDate)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["QuestID"], row["CompletionDate"]))

    print("  ✔ Seeded CharacterQuest")


def seed():
    init_db()
    conn = get_db()          # was: get_connection() - does not exist
    cursor = conn.cursor()

    try:
        seed_lookup_tables(cursor)
        seed_core_data(cursor)
        conn.commit()
        print("\nSeed complete.")
    except Exception as e:
        conn.rollback()
        print(f"\nSeed failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
