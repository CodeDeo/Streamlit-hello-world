"""Level-one character data and calculations for the 2014 rules."""
from random import randint

ABILITIES = ("Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma")
STANDARD_ARRAY = (15, 14, 13, 12, 10, 8)
CLASSES = {
    "Barbarian": (12, ("Strength", "Constitution")),
    "Bard": (8, ("Dexterity", "Charisma")),
    "Cleric": (8, ("Wisdom", "Charisma")),
    "Druid": (8, ("Intelligence", "Wisdom")),
    "Fighter": (10, ("Strength", "Constitution")),
    "Monk": (8, ("Strength", "Dexterity")),
    "Paladin": (10, ("Wisdom", "Charisma")),
    "Ranger": (10, ("Strength", "Dexterity")),
    "Rogue": (8, ("Dexterity", "Intelligence")),
    "Sorcerer": (6, ("Constitution", "Charisma")),
    "Warlock": (8, ("Wisdom", "Charisma")),
    "Wizard": (6, ("Intelligence", "Wisdom")),
}
ANCESTRIES = {
    "Human": ({ability: 1 for ability in ABILITIES}, 30),
    "High Elf": ({"Dexterity": 2, "Intelligence": 1}, 30),
    "Hill Dwarf": ({"Constitution": 2, "Wisdom": 1}, 25),
    "Lightfoot Halfling": ({"Dexterity": 2, "Charisma": 1}, 25),
    "Rock Gnome": ({"Intelligence": 2, "Constitution": 1}, 25),
    "Tiefling": ({"Charisma": 2, "Intelligence": 1}, 30),
    "Half-Orc": ({"Strength": 2, "Constitution": 1}, 30),
}


def roll_scores():
    return [tuple(sorted(randint(1, 6) for _ in range(4))) for _ in ABILITIES]


def character_stats(character_class, ancestry, base_scores):
    bonuses, speed = ANCESTRIES[ancestry]
    hit_die, proficient_saves = CLASSES[character_class]
    rows = []
    for ability, base in zip(ABILITIES, base_scores, strict=True):
        bonus = bonuses.get(ability, 0)
        score = base + bonus
        modifier = (score - 10) // 2
        rows.append({
            "Ability": ability,
            "Base": base,
            "Bonus": bonus,
            "Score": score,
            "Modifier": modifier,
            "Saving throw": modifier + (2 if ability in proficient_saves else 0),
        })
    modifiers = {row["Ability"]: row["Modifier"] for row in rows}
    hp = max(1, hit_die + modifiers["Constitution"]) + (ancestry == "Hill Dwarf")
    return rows, hp, modifiers["Dexterity"], speed
