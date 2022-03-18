import zipfile
import json

pack_format = 9

def addToLootTable(lootfilename, weight = 1, pool = 0, indent = None):
    with open('base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())
    lootjson['pools'][pool]['entries'].append({
        'type': 'loot_table',
        'weight': weight,
        "name": "babel:books"
    })
    return json.dumps(lootjson, indent=indent, ensure_ascii=False)

def getBooksJsonString(loottable, indent = None):
    return json.dumps(loottable, indent=indent, ensure_ascii=False)

def buildDatapack(filename, argsloottable, loottable, indent = None):
    zf = zipfile.ZipFile(filename, mode='w')
    zf.writestr('pack.mcmeta', json.dumps({
        "pack": {
            "pack_format": pack_format,
            "description": "Add pre-written books to your vanilla world. https://github.com/JiFish/babel"
        }
    }, indent=indent, ensure_ascii=False))
    zf.writestr('data/babel/loot_tables/books.json', getBooksJsonString(loottable, indent=indent))
    if 'stronghold' not in argsloottable:
        print ("Adding to Stronghold Library loot table.")
        zf.writestr('data/minecraft/loot_tables/chests/stronghold_library.json', addToLootTable('stronghold_library.json',15, indent=indent))
    if 'mansion' not in argsloottable:
        print ("Adding to Woodland Mansion loot table.")
        zf.writestr('data/minecraft/loot_tables/chests/woodland_mansion.json', addToLootTable('woodland_mansion.json',5, indent=indent))
    if 'village' not in argsloottable:
        print ("Adding to Village loot table.")
        zf.writestr('data/minecraft/loot_tables/chests/village/village_desert_house.json', addToLootTable('village_desert_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_tables/chests/village/village_plains_house.json', addToLootTable('village_plains_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_tables/chests/village/village_savanna_house.json', addToLootTable('village_savanna_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_tables/chests/village/village_snowy_house.json', addToLootTable('village_snowy_house.json',3, indent=indent))
        zf.writestr('data/minecraft/loot_tables/chests/village/village_taiga_house.json', addToLootTable('village_taiga_house.json',3, indent=indent))
    if 'fishing' not in argsloottable:
        print ("Adding to Fishing Treasure loot table.")
        zf.writestr('data/minecraft/loot_tables/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1, indent=indent))
    if 'zombie' not in argsloottable:
        print ("Adding to Zombie drop loot table.")
        zf.writestr('data/minecraft/loot_tables/entities/zombie.json', addToLootTable('zombie.json',1,1, indent=indent))
    zf.close()
