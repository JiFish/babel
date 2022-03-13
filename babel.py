import zipfile
import json
import argparse
import sys

isCompiled = getattr(sys, 'frozen', False)
isUsingDefaults = (len(sys.argv) < 2)
validLootTableList = ['fishing', 'village', 'mansion', 'stronghold', 'zombie']
greeting = "Babel Book Loot Generator, v0.4%s" % (' (Windows)' if isCompiled else '')

print("\n"+greeting)
print("="*len(greeting)+"\n")

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Optional output zip filename. Default: babel.zip', nargs='?', default='babel.zip')
parser.add_argument('-d', dest="loottable", default=[], action='append', help='Disable adding books to one of the following loot tables: '+
                    ', '.join(validLootTableList)+'. Can be repeated to disable more than one.')
parser.add_argument('-c', '--clean', help='Indent output JSON files.', action='store_true')
if isCompiled:
    parser.add_argument('-!', '--no-wait', help="Don't wait for user input at the end of the build. Triggered automatically by using any other argument.",
                        action='store_true')
args = parser.parse_args()

if set(args.loottable).issubset(validLootTableList) == False:
    print("ERROR: Invalid input on -d argument\n")
    parser.print_help()
    exit(1)

if args.clean:
    indent = 4
else:
    indent = None

if isUsingDefaults:
    print("Using default configuration, for more options try %s -h\n" % sys.argv[0])

print ("Importing Books...")
from build_loottable import loottable
print ("Found %d books." % len(loottable['pools'][0]['entries']))

def addToLootTable(lootfilename, weight = 1, pool = 0):
    global indent
    with open('base_loot_tables/'+lootfilename, 'r') as lootfile:
        lootjson = json.loads(lootfile.read())
    lootjson['pools'][pool]['entries'].append({
        'type': 'loot_table',
        'weight': weight,
        "name": "babel:books"
    })
    return json.dumps(lootjson, indent=indent, ensure_ascii=False)

print ("Building datapack...")
zf = zipfile.ZipFile(args.filename, mode='w')
zf.writestr('pack.mcmeta', json.dumps({
    "pack": {
        "pack_format": 7,
        "description": "Add pre-written books to your vanilla world"
    }
}, indent=indent, ensure_ascii=False))
zf.writestr('data/babel/loot_tables/books.json', json.dumps(loottable, indent=indent, ensure_ascii=False))
if 'stronghold' not in args.loottable:
    print ("Adding to Stronghold Library loot table.")
    zf.writestr('data/minecraft/loot_tables/chests/stronghold_library.json', addToLootTable('stronghold_library.json',15))
if 'mansion' not in args.loottable:
    print ("Adding to Woodland Mansion loot table.")
    zf.writestr('data/minecraft/loot_tables/chests/woodland_mansion.json', addToLootTable('woodland_mansion.json',5))
if 'village' not in args.loottable:
    print ("Adding to Village loot table.")
    zf.writestr('data/minecraft/loot_tables/chests/village/village_desert_house.json', addToLootTable('village_desert_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_plains_house.json', addToLootTable('village_plains_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_savanna_house.json', addToLootTable('village_savanna_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_snowy_house.json', addToLootTable('village_snowy_house.json',3))
    zf.writestr('data/minecraft/loot_tables/chests/village/village_taiga_house.json', addToLootTable('village_taiga_house.json',3))
if 'fishing' not in args.loottable:
    print ("Adding to Fishing Treasure loot table.")
    zf.writestr('data/minecraft/loot_tables/gameplay/fishing/treasure.json', addToLootTable('treasure.json',1))
if 'zombie' not in args.loottable:
    print ("Adding to Zombie drop loot table.")
    zf.writestr('data/minecraft/loot_tables/entities/zombie.json', addToLootTable('zombie.json',1,1))
zf.close()
print ("\nDatapack build complete! Copy %s to your world's datapack directory." % args.filename)

if isCompiled and isUsingDefaults:
    input("\nPress ENTER or close this window.")
