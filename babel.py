import argparse
import sys
import yaml;
from build_datapack import *
from build_loottable import *

def loadAndValidateYaml(yamlFilePath):
    # Load the YAML file
    with open(yamlFilePath, 'r') as file:
        data = yaml.safe_load(file)
    
    # Define the required fields and their types
    requiredFields = {
        'output-filename': str,
        'add-crafting-recipe': bool,
        'add-fishing-loot': bool,
        'add-village-loot': bool,
        'add-mansion-loot': bool,
        'add-stronghold-loot': bool,
        'add-zombie-drop': bool,
        'replace-hero-of-the-village-gift': bool,
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
        
        value = data[field]
        
        if not isinstance(value, fieldType):
            raise TypeError(f"Incorrect type for field '{field}'. Expected {fieldType.__name__}, got {type(value).__name__}.")
        
        # For float fields, ensure they are between 0 and 1
        if fieldType is float and not (0 <= value <= 1):
            raise ValueError(f"Field '{field}' must be between 0 and 1. Got {value}.")
    
    return data

isCompiled = getattr(sys, 'frozen', False)
greeting = "Babel Book Loot Generator, v1.1%s" % (' (Windows)' if isCompiled else '')

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Optional config filename. (default: %(default)s)', nargs='?', default='config.yaml')
parser.add_argument('-v', '--version', action='version', version=greeting)
if isCompiled:
    parser.add_argument('-!', '--no-wait', action='store_true',
                        help="Don't wait for user input when finished.")
args = parser.parse_args()

print("\n"+greeting)
print("="*len(greeting)+"\n")

print("Using configuration: %s." % args.filename)
config = loadAndValidateYaml(args.filename)

try:
    loottable = buildLootTable('books/', config)
    print ("Found %d books." % len(loottable['pools'][0]['entries']))

    print ("Building datapack...")
    buildDatapack(config, loottable)
    print ("\nDatapack build complete! Copy %s to your world's datapack directory." % config['output-filename'])

except Exception as e:
    print("\nError: "+str(e))

finally:
    if isCompiled and not args.no_wait:
        input("\nPress ENTER or close this window.")
