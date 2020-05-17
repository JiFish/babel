import zipfile
import json
import argparse
from sys import argv

print ("Importing Books...")
from build_lootable import loottable

def addToLootTable(lootfilename, weight = 1):
    global indent
    with open('base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())
    lootjson['pools'][0]['entries'].append({
        'type': 'loot_table',
        'weight': weight,
        "name": "babel:books"
    })
    return json.dumps(lootjson, indent=indent)
    
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Output zip file', nargs='?', default='babel.zip')
parser.add_argument('-c', '--clean', help='Indent output JSON files', action='store_true')
parser.add_argument('--no-fishing', dest="fishing", help='Disable adding books to fishing loot', action='store_false')
parser.add_argument('--no-village', dest="village", help='Disable adding books to village loot', action='store_false')
parser.add_argument('--no-mansion', dest="mansion", help='Disable adding books to woodland mansion loot', action='store_false')
parser.add_argument('--no-stronghold', dest="stronghold", help='Disable adding books to stronghold library loot', action='store_false')
args = parser.parse_args()

if len(argv) < 2:
    print("Using default configuration, for more options try build.py -h")

if args.clean:
    indent = 4
else:
    indent = None

print ("Writing to "+args.filename+"...")
zf = zipfile.ZipFile(args.filename, mode='w')
zf.writestr('pack.mcmeta', json.dumps({
    "pack": {
        "pack_format": 5,
        "description": "Add pre-written books to your vanilla world"
    }
}, indent=indent))
zf.writestr('data/babel/loot_tables/books.json', json.dumps(loottable, indent=indent))
if args.stronghold:
    zf.writestr('data/minecraft/loot_tables/chests/stronghold_library.json', addToLootTable('stronghold_library.json',15))
if args.mansion:
    zf.writestr('data/minecraft/loot_tables/chests/woodland_mansion.json', addToLootTable('woodland_mansion.json',5))
if args.village:
    zf.writestr('data/minecraft/loot_tables/chests/village/village_desert_house.json', addToLootTable('village_desert_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_plains_house.json', addToLootTable('village_plains_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_savanna_house.json', addToLootTable('village_savanna_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_snowy_house.json', addToLootTable('village_snowy_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_taiga_house.json', addToLootTable('village_taiga_house.json',3))
if args.fishing:
    zf.writestr('data/minecraft/loot_tables/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1))
zf.close()
print ("Complete.")
