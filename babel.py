# By Joseph "JiFish" Fowler. All rights reserved.

import argparse
import sys
import yaml;
import os;
from build_datapack import *
from build_loottable import *
from minecraft_extract import extractFilesFromJar

def loadAndValidateYaml(yamlFilePath):
    # Load the YAML file
    with open(yamlFilePath, 'r') as file:
        data = yaml.safe_load(file)
    
    # Define the required fields and their types
    requiredFields = {
        'output-filename': str,
        'books-path': str,
        'add-crafting-recipe': bool,
        'add-fishing-loot': bool,
        'add-village-loot': bool,
        'add-mansion-loot': bool,
        'add-stronghold-loot': bool,
        'add-zombie-drop': bool,
        'replace-hero-of-the-village-gift': bool,
        'add-lost-libraries': bool,
        'indent-output': bool,
        'copy-of-copy-chance': float,
        'copy-of-original-chance': float,
        'original-chance': float,
    }
    
    # Check for unrecognized fields
    for field in data:
        if field not in requiredFields:
            raise ValueError(f"Unrecognized field: {field}")
    
    # Validate the fields
    for field, fieldType in requiredFields.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        
        # Floats can also be ints, convert now
        if type(data[field]) == int:
            data[field] = float(data[field])
        
        value = data[field]
        if not isinstance(value, fieldType):
            raise TypeError(f"Incorrect type for field '{field}'. Expected {fieldType.__name__}, got {type(value).__name__}.")
        
        # For float fields, ensure they are between 0 and 1
        if fieldType is float and not (0 <= value <= 1):
            raise ValueError(f"Field '{field}' must be between 0 and 1. Got {value}.")
    
    return data

isCompiled = getattr(sys, 'frozen', False)
version = "v2-be%s" % (' (Windows)' if isCompiled else '')
minecraft_version = "1.21.4"

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Optional config filename. (default: %(default)s)', nargs='?', default='config.yaml')
parser.add_argument('-v', '--version', action='version', version=version)
parser.add_argument('-i', '--indent', action='store_true', help="Indent output json files. Overrides config field.")
parser.add_argument('-a', '--append-version', action='store_true', help="Append babel version number to output filename.")

if isCompiled:
    parser.add_argument('-!', '--no-wait', action='store_true',
                        help="Don't wait for user input when finished.")
    # Handle windows style help arg
    if len(sys.argv) == 2 and sys.argv[1] == '/?':
        sys.argv[1] = '--help'

args = parser.parse_args()

print("")
print("░█▀▄░█▀█░█▀▄░█▀▀░█░░░░░█▀▄░█▀█░█▀█░█░█░░░█░░░█▀█░█▀█░▀█▀")
print("░█▀▄░█▀█░█▀▄░█▀▀░█░░░░░█▀▄░█░█░█░█░█▀▄░░░█░░░█░█░█░█░░█░")
print("░▀▀░░▀░▀░▀▀░░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░░▀░ " + version)
print('By JiFish. email: %s' % 'ku.oc.hsifij@eoj'[::-1])
print("")

print("Using configuration: %s.\n" % args.filename)

try:
    config = loadAndValidateYaml(args.filename)

    # indent arg overrides config field
    if args.indent:
        config['indent-output'] = True

    # Append version alters 'output-filename'
    if args.append_version:
        filename, extension = os.path.splitext(config['output-filename'])
        config['output-filename'] = filename + '_' + version + extension

    extractFilesFromJar(minecraft_version)

    loottable = buildLootTable(config)

    print ("\nBuilding data pack...")
    buildDatapack(config, loottable, version)
    print ("Data pack build complete!\n\nCopy %s to your world's 'datapacks' directory." % config['output-filename'])

except Exception as e:
    print("\nError: "+str(e))

finally:
    if isCompiled and not args.no_wait:
        input("\nPress ENTER or close this window.")
