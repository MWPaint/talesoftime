"""
seed.py - Populates all reference / lookup tables with initial data.
Run once: python database/seed.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from extensions import db
from models.models import (
    CharacterClass, Species, Alignment,
    ItemType, Rarity, Region, Difficulty,
    Character, Item, Quest, Inventory, CharacterQuest
)


LOOKUP_SEED_DATA = {
    CharacterClass: [
        {"ClassName": "Warrior", "Description": "A powerful melee fighter."},
    ],
    Species: [
        {"SpeciesName": "Human"},
    ],
    Alignment: [
        {"AlignmentName": "Lawful Good"},
    ],
    ItemType: [
        {"TypeName": "Weapon"},    
    ],
    Rarity: [
        {"RarityName": "Common"},
    ],
    Region: [
        {"RegionName": "The Verdant Vale"},
    ],
    Difficulty: [
        {"DifficultyName": "Novice"},
    ],
}


def seed_lookup_tables():
    for model, rows in LOOKUP_SEED_DATA. items():
        if model.query.count() == 0:
            for row in rows:
                db.session.add(model(**row))
            print(f" Seeded {model.__tablename__}")
        else:
            print(f" Skipped {model.__tablename__} (already has data)")
    db.session.commit()








    #Lookup helpers
    classes = {c.ClassName: c for c in CharacterClass.query.all()}
    species = {s.SpeciesName: s for s in Species.query.all()}
    alignments = {a.AlignmentName: a for a in Alignment.query.all()}
    item_types = {i.TypeName: i for i in ItemType.query.all()}
    rarities = {r.RarityName: r for r in Rarity.query.all()}
    regions = {r.RegionName: r for r in Region.query.all()}
    difficulties = {d.DifficultyName: d for d in Difficulty.query.all()}

    #Characters
    character_rows = [
        {
            "CharacterName": "Thorin Ironblade",
            "ClassID": classes["Warrior"].ClassID,
            "Species": species["Dwarf"].SpeciesID,
            "AlignmentID": alignments["Lawful Good"].AlignmentsID,
            "Level": 12,
        },
    ]

    characters = []
    for row in character_rows:
        character = Character(**row)
        db.session.add(character)
        characters.append(character)

    db.session.commit()
    print(" Seeded Character")

    character_map = {c.CharacterName: c for c in Character.query.all()}

    #Items
    item_rows = [
        {
            "ItemName": "Iron Sword",
            "ItemTypeID": item_types["Weapon"].ItemTypeID,
            "RarityID": rarities["Common"].RarityID,
        },
    ]

    for row in item_rows:
        db.session.add(Item(**row))

    db.session.commit()
    print(" Seeded Item")

    item_map = {i.ItemName: i for i in Item.query.all()}

    #Quests
    quest_rows = [
        {
            "QuestName": "Defenc the Vale",
            "RegionID": regions["The Verdant Vale"].RegionID,
            "DifficultyID": difficulties["Journeyman"].DifficultyID,
        },
    ]

    for row in quest_rows:
        db.session.add(Quest(**row))

    db.session.commit()
    print(" Seeded Quest")

    quest_map = {q.QuestName: q for q in Quest.query.all()}

    #Inventory
    inventory_rows = [
        {
            "CharacterID": character_map["Thorin Ironblade"].CharacterID,
            "ItemID": item_map["Iron Sword"].ItemID,
            "Quantity": 1,
        },
    ]

    for row in inventory_rows:
        db.session.add(Inventory(**row))

    db.session.commit()
    print(" Seeded Inventory")

    #CharacterQuest
    character_quest_rows = [
        {
            "CharacterID": character_map["Thorin Ironblade"].CharacterID,
            "QuestID": quest_map["Defend the Vale"].QuestID,
            "ComplationDate": datetime(2026, 1, 12, 14, 30),
        },
    ]

    for row in character_quest_rows:
        db.session.add(CharacterQuest(**row))

    db.session.commit()
    print(" Seeded CharacterQuest")


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_lookup_tables()
        seed_core_data()
        print("\nSeed Complete")


if __name__ == "__main__":
    seed()
