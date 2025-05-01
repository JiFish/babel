# By Joseph "JiFish" Fowler. All rights reserved.

import zipfile
import json
from build_loottable import buildLootTable, buildTestLootTables
from build_knowlege_books import buildKnowledgeBooksTable

# Use zlib if we have it
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED

min_pack_format = 57
pack_format = 71

extracted_data_directory = None


def addToLootTable(lootfilename, weight=1, pool=0, guaranteedFind=False, quality=False, indent=None):
    with open(f"{extracted_data_directory}/base_loot_tables/{lootfilename}", 'r') as lootfile:
        lootjson = json.loads(lootfile.read())

    # Basic loot pool entry
    loot_pool_entry = {
        'type': 'minecraft:loot_table',
        'weight': weight,
        "value": "babel:books"
    }

    # Give the book the a quality
    if quality:
        loot_pool_entry["functions"] = [{
            "function": "minecraft:set_lore",
            "lore": [{
                "text": quality,
                "type": "text",
                "color": "gray",
                "italic": False
            }],
            "mode": "replace_all"
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


def getBooksJsonString(loottable, indent=None):
    return json.dumps(loottable, indent=indent, ensure_ascii=False)

# Load the file, parse json then spit back out
# Re-indents (or minimizes) the json as requested
# Also checks the json is valid   
def getFileJson(filename, indent = None, string = True):
    with open(filename) as jsonFile:
        jsonValue = json.load(jsonFile)
    if not string:
        return jsonValue
    return json.dumps(jsonValue, indent=indent)


def buildDatapack(config, version, extracted_data_dir):
    global extracted_data_directory
    extracted_data_directory = extracted_data_dir

    indent = 2 if config['indent-output'] else None

    print("Adding pack meta data.")
    zf = zipfile.ZipFile(config['output-filename'], mode='w', compression=compression)
    zf.writestr('pack.mcmeta', json.dumps({
        "pack": {
            "description": version + ". Adds pre-written books to loot. https://github.com/JiFish/babel",
            "pack_format": pack_format,
            "supported_formats": [min_pack_format, pack_format]
        }
    }, indent=indent, ensure_ascii=False))
    zf.write('data/pack.png', 'pack.png')

    loottable = buildLootTable(config)
    zf.writestr('data/babel/loot_table/books.json', getBooksJsonString(loottable, indent=indent))

    if config['add-metabox']:
        for name, testtable in buildTestLootTables(config).items():
            zf.writestr(f"data/babel/loot_table/{name}.json", getBooksJsonString(testtable, indent=indent))
    if config['add-stronghold-loot']:
        print("Adding to Stronghold Library loot table.")
        zf.writestr(
            'data/minecraft/loot_table/chests/stronghold_library.json',
            addToLootTable('stronghold_library.json', config['weights']['stronghold-library'], guaranteedFind=True, indent=indent)
        )
    if config['add-mansion-loot']:
        print("Adding to Woodland Mansion loot table.")
        zf.writestr(
            'data/minecraft/loot_table/chests/woodland_mansion.json',
            addToLootTable('woodland_mansion.json', config['weights']['woodland-mansion'], indent=indent)
        )
    if config['add-village-loot']:
        print("Adding to Village loot tables.")
        for table in ['village_desert_house', 'village_savanna_house', 'village_plains_house', 'village_taiga_house', 'village_snowy_house']:
            zf.writestr(
                f'data/minecraft/loot_table/chests/village/{table}.json',
                addToLootTable(f'{table}.json', config['weights']['village'], indent=indent)
            )
    if config['add-fishing-loot']:
        print("Adding to Fishing Treasure loot table.")
        zf.writestr(
            'data/minecraft/loot_table/gameplay/fishing/treasure.json',
            addToLootTable('treasure.json', config['weights']['fishing'], quality="Waterlogged", indent=indent)
        )
    if config['add-zombie-drop']:
        print("Adding to Zombie drop loot table.")
        zf.writestr(
            'data/minecraft/loot_table/entities/zombie.json',
            addToLootTable('zombie.json', config['weights']['zombie'], 1, indent=indent)
        )
    if config['replace-hero-of-the-village-gift']:
        print("Replacing Librarian's Hero of the village gift.")
        zf.writestr('data/minecraft/loot_table/gameplay/hero_of_the_village/librarian_gift.json', getFileJson('data/librarian_gift.json', indent=indent))
    if config['add-crafting-recipe']:
        print("Adding crafting recipe.")
        zf.writestr('data/babel/loot_table/crafted_chest.json', getFileJson('data/crafted_chest.json', indent=indent))
        zf.writestr('data/babel/recipe/babel_book_recipe.json', getFileJson('data/babel_book_recipe.json', indent=indent))
    if config['add-lost-libraries']:
        print("Adding Lost Libraries to worldgen.")
        # Loot Tables
        zf.writestr('data/babel/loot_table/lost_library_chest.json', getFileJson('data/lost_library_chest.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_chest_poor.json', getFileJson('data/lost_library_chest_poor.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_chest_good.json', getFileJson('data/lost_library_chest_good.json', indent=indent))
        zf.writestr('data/babel/loot_table/lost_library_pot.json', getFileJson('data/lost_library_pot.json', indent=indent))
        # Knowlege and Junk book loot tables
        knowlege_book = buildKnowledgeBooksTable(extracted_data_directory)
        zf.writestr('data/babel/loot_table/knowlege_book.json', json.dumps(knowlege_book, indent=indent))
        loottable = buildLootTable({'books-path': 'junk_books/', 'copy-of-copy-chance': 0, 'copy-of-original-chance': 0, 'original-chance': 0}, 'Creating junk loot table...')
        zf.writestr('data/babel/loot_table/junk_books.json', json.dumps(loottable, indent=indent))

        # Add structures, set, pools, and tags
        POOLS = ['tuff', 'stone', 'sandstone']
        VARIANTS = 4
        lost_library_struc = getFileJson('data/lost_library.json', string=False)
        pool_struc = getFileJson('data/lost_library_pool.json', string=False)
        set_struc = getFileJson('data/lost_library_set.json', string=False)
        set_struc['structures'] = []
        lost_library_tag = {"values": []}
        for pool in POOLS:
            set_struc['structures'].append({"structure": f"babel:lost_library_{pool}", "weight": 1})
            lost_library_tag['values'].append(f"babel:lost_library_{pool}")
            lost_library_struc['start_pool'] = f"babel:lost_library_pool_{pool}"
            lost_library_struc['biomes'] = f"#babel:has_structure/lost_library_{pool}"
            zf.writestr(f"data/babel/worldgen/structure/lost_library_{pool}.json", json.dumps(lost_library_struc, indent=indent))
            for i in range(VARIANTS):
                pool_struc['elements'][i]['element']['location'] = f"babel:lost_library_{pool}_v{i}"
                zf.write(f"data/structure/lost_library_{pool}_v{i}.nbt", f"data/babel/structure/lost_library_{pool}_v{i}.nbt")
            zf.writestr(f"data/babel/worldgen/template_pool/lost_library_pool_{pool}.json", json.dumps(pool_struc, indent=indent))
            zf.writestr(f"data/babel/tags/worldgen/biome/has_structure/lost_library_{pool}.json", getFileJson(f"data/biome/lost_library_{pool}.json", indent=indent))
        zf.writestr('data/babel/tags/worldgen/structure/lost_library.json', json.dumps(lost_library_tag, indent=indent))
        zf.writestr('data/babel/worldgen/structure_set/lost_library_set.json', json.dumps(set_struc, indent=indent))
        
    zf.close()
