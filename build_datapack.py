# By Joseph "JiFish" Fowler. All rights reserved.

import zipfile
import json

# Use zlib if we have it
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED

min_pack_format = 45
pack_format = 48

def addToLootTable(lootfilename, weight = 1, pool = 0, guaranteedFind = False, indent = None):
    with open('base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())

    # Add to loot specified pool
    lootjson['pools'][pool]['entries'].append({
        'type': 'minecraft:loot_table',
        'weight': weight,
        "value": "babel:books"
    })

    # Add a new, guaranteed pool
    if guaranteedFind:
        lootjson['pools'].append({
            "bonus_rolls": 0.0,
            "entries": [
                {
                    "type": "minecraft:loot_table",
                    "value": "babel:books"
                }
            ],
            "rolls": 1.0
        })

    return json.dumps(lootjson, indent=indent, ensure_ascii=False)

def getBooksJsonString(loottable, indent = None):
    return json.dumps(loottable, indent=indent, ensure_ascii=False)

# Load the file, parse json then spit back out
# Re-indents (or minimizes) the json as requested
# Also checks the json is valid   
def getFileJson(filename, indent = None):
    with open(filename) as jsonFile:
        return json.dumps(json.load(jsonFile), indent=indent)

def buildDatapack(config, loottable, version):
    indent = 2 if config['indent-output'] else None

    zf = zipfile.ZipFile(config['output-filename'], mode='w', compression=compression)
    zf.writestr('pack.mcmeta', json.dumps({
        "pack": {
            "description": version + ". Adds pre-written books to loot. https://github.com/JiFish/babel",
            "pack_format": pack_format,
            "supported_formats": [min_pack_format, pack_format]
        }
    }, indent=indent, ensure_ascii=False))
    print("Creating babel:books loot table.")
    zf.writestr('data/babel/loot_table/books.json', getBooksJsonString(loottable, indent=indent))
    if config['add-stronghold-loot']:
        print("Adding to Stronghold Library loot table.")
        zf.writestr('data/minecraft/loot_table/chests/stronghold_library.json', addToLootTable('stronghold_library.json',15, guaranteedFind=True, indent=indent))
    if config['add-mansion-loot']:
        print("Adding to Woodland Mansion loot table.")
        zf.writestr('data/minecraft/loot_table/chests/woodland_mansion.json', addToLootTable('woodland_mansion.json',5, indent=indent))
    if config['add-village-loot']:
        print("Adding to Village loot tables.")
        zf.writestr('data/minecraft/loot_table/chests/village/village_desert_house.json', addToLootTable('village_desert_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_plains_house.json', addToLootTable('village_plains_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_savanna_house.json', addToLootTable('village_savanna_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_snowy_house.json', addToLootTable('village_snowy_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_table/chests/village/village_taiga_house.json', addToLootTable('village_taiga_house.json',3, indent=indent))
    if config['add-fishing-loot']:
        print("Adding to Fishing Treasure loot table.")
        zf.writestr('data/minecraft/loot_table/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1, indent=indent))
    if config['add-zombie-drop']:
        print("Adding to Zombie drop loot table.")
        zf.writestr('data/minecraft/loot_table/entities/zombie.json', addToLootTable('zombie.json',1,1, indent=indent))
    if config['replace-hero-of-the-village-gift']:
        print("Replacing Librarian's Hero of the village gift.")
        zf.writestr('data/minecraft/loot_table/gameplay/hero_of_the_village/librarian_gift.json', getFileJson('extras/librarian_gift.json', indent=indent))
    if config['add-crafting-recipe']:
        print("Adding crafting recipe.")
        zf.writestr('data/babel/recipe/babel_book_recipe.json', getFileJson('extras/babel_book_recipe.json', indent=indent))
    zf.close()
