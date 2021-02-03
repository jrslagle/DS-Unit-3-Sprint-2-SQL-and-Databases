
# Look at the charactercreator_character table
# GET_CHARACTERS = """
# SELECT *
# FROM charactercreator_character;
# """

# How many total Characters are there? (302)
TOTAL_CHARACTERS = """
SELECT COUNT(*) as number_of_characters
FROM charactercreator_character;
"""

# How many of each specific subclass?
# TOTAL_SUBCLASS = """
# SELECT
# 	(SELECT COUNT(*) FROM charactercreator_necromancer) AS necros,
# 	(SELECT COUNT(*) FROM charactercreator_mage) AS mages,
# 	(SELECT COUNT(*) FROM charactercreator_thief) AS thiefs,
# 	(SELECT COUNT(*) FROM charactercreator_cleric) AS clerics,
# 	(SELECT COUNT(*) FROM charactercreator_fighter) AS fighters;
# """

CLASS = "SELECT COUNT(*) FROM charactercreator_"

# How many total Items? (174)
TOTAL_ITEMS = """
SELECT COUNT(item_id) as items
FROM armory_item;
"""

# How many of the Items are weapons? (37)
WEAPONS = """
SELECT COUNT(item_ptr_id)
FROM armory_weapon;
"""

# How many of the items are not weapons? (137)
NON_WEAPONS = """
SELECT COUNT(items.name)
FROM armory_item as items
WHERE items.item_id NOT IN(
SELECT armory_weapon.item_ptr_id
FROM armory_weapon);
"""

# How many Items does each character have? (Return first 20 rows)
CHARACTER_ITEMS = """
SELECT character.name as "character_name", COUNT(inventory.id) as "#_of_items"
FROM charactercreator_character AS character, charactercreator_character_inventory AS inventory
WHERE character.character_id = inventory.character_id
GROUP BY character.name
ORDER BY character.name
LIMIT 20;
"""

# How many Weapons does each character have? (Return first 20 rows)
CHARACTER_WEAPONS = """
SELECT character.name as "character_name", COUNT(weapon.item_ptr_id) as "#_of_weapons"
FROM charactercreator_character AS character, charactercreator_character_inventory AS inventory, armory_weapon as weapon
WHERE character.character_id = inventory.character_id AND inventory.item_id = weapon.item_ptr_id
GROUP BY character.name
ORDER BY character.name
LIMIT 20;
"""

# On average, how many Items does each Character have? (3.02)
AVG_CHARACTER_ITEMS = """
SELECT
	AVG("#_of_items") as "avg_#_of_items"
FROM
(
	SELECT
		COUNT(inventory.id) AS "#_of_items"
	FROM
		charactercreator_character AS character,
		charactercreator_character_inventory AS inventory
		WHERE
			character.character_id = inventory.character_id
		GROUP BY character.name
);
"""

# On average, how many Weapons does each character have? (0.67)
AVG_CHARACTER_WEAPONS = """
SELECT
	AVG(weapon_count) as avg_weapons_per_char
FROM (
	SELECT
		character.character_id,
		COUNT(DISTINCT weapon.item_ptr_id) as weapon_count
	FROM
		charactercreator_character AS character
		LEFT JOIN charactercreator_character_inventory inventory  -- characters may have zero items
			ON character.character_id = inventory.character_id
		LEFT JOIN armory_weapon weapon  -- many items are not weapons, so only retain weapons
			ON inventory.item_id = weapon.item_ptr_id
		GROUP BY character.character_id
) subq;
"""

