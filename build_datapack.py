# By Joseph "JiFish" Fowler. All rights reserved.

import zipfile
import json
import copy
from glob import glob

# Use zlib if we have it
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED

min_pack_format = 57
pack_format = 61

def addToLootTable(lootfilename, weight = 1, pool = 0, guaranteedFind = False, forceTattered = False, indent = None):
    with open('data_extracted/base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())

    # Basic loot pool entry
    loot_pool_entry = {
        'type': 'minecraft:loot_table',
        'weight': weight,
        "value": "babel:books"
    }

    # Force the book to be tattered
    if forceTattered:
        loot_pool_entry["functions"] = [{
            "function": "minecraft:set_book_cover",
            "generation": 3
        }]

    # Add to loot specified pool
    lootjson['pools'][pool]['entries'].append(loot_pool_entry)

    # Add a new, guaranteed pool
    if guaranteedFind:
        lootjson['pools'].append({
            "bonus_rolls": 0.0,
            "entries": [loot_pool_entry],
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
    zf.write('pack.png', 'pack.png')
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
        zf.writestr('data/minecraft/loot_table/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1, forceTattered=True, indent=indent))
    if config['add-zombie-drop']:
        print("Adding to Zombie drop loot table.")
        zf.writestr('data/minecraft/loot_table/entities/zombie.json', addToLootTable('zombie.json',1,1, indent=indent))
    if config['replace-hero-of-the-village-gift']:
        print("Replacing Librarian's Hero of the village gift.")
        zf.writestr('data/minecraft/loot_table/gameplay/hero_of_the_village/librarian_gift.json', getFileJson('data/librarian_gift.json', indent=indent))
    if config['add-crafting-recipe']:
        print("Adding crafting recipe.")
        zf.writestr('data/babel/loot_table/crafted_chest.json', getFileJson('data/crafted_chest.json', indent=indent))
        zf.writestr('data/babel/recipe/babel_book_recipe.json', getFileJson('data/babel_book_recipe.json', indent=indent))
    if config['add-lost-libraries']:
        print("Adding Lost Libraries to worldgen.")
        loottable = buildLootTable({'books-path': 'junk_books/', 'copy-of-copy-chance': 0, 'copy-of-original-chance': 0, 'original-chance': 0}, True)
        zf.writestr('data/babel/loot_table/junk_books.json', json.dumps(loottable, indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_chest.json', getFileJson('data/lost_library_chest.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_chest_poor.json', getFileJson('data/lost_library_chest_poor.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_chest_good.json', getFileJson('data/lost_library_chest_good.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_pot.json', getFileJson('data/lost_library_pot.json', indent=indent))
        zf.writestr('data/babel/worldgen/structure_set/lost_library_set.json', getFileJson('data/lost_library_set.json', indent=indent))
        zf.writestr('data/babel/worldgen/template_pool/lost_library_pool.json', getFileJson('data/lost_library_pool.json', indent=indent))
        zf.writestr('data/babel/worldgen/structure/lost_library.json', getFileJson('data/lost_library.json', indent=indent))
        zf.write('data/lost_library.nbt', 'data/babel/structure/lost_library.nbt')
        with open('data/knowlege_book.json') as jsonFile:
            kb = json.load(jsonFile)
        item = kb["pools"][0]["entries"][0]
        newpool = {}
        for recp in glob('data_extracted/base_recipe/*.json'):
            name = recp.replace('\\', '/').split('/')[-1]  # Get the file name with extension
            name = name[:-5]  # Remove the last 5 characters (".json")
            with open(recp) as jsonFile:
                recp_json = json.load(jsonFile)
            if recp_json['type'] not in ['minecraft:crafting_shaped', 'minecraft:crafting_shapeless']:
                continue
                
            if 'group' in recp_json:
                group_name = recp_json['group']
            else:
                group_name = name
            
            if group_name not in newpool:
                newitem = copy.deepcopy(item)
                newitem["functions"][0]["components"]["minecraft:recipes"][0] = "minecraft:" + name
                newitem["functions"][0]["components"]["minecraft:lore"][0] = "\""+group_name.replace("_", " ").title()+"\""
                newpool[group_name] = newitem
            else:
                newpool[group_name]["functions"][0]["components"]["minecraft:recipes"].append("minecraft:" + name)
        kb["pools"][0]["entries"] = list(newpool.values())
        zf.writestr('data/babel/loot_table/knowlege_book.json', json.dumps(kb, indent=indent))
    zf.close()
