# By Joseph "JiFish" Fowler. All rights reserved.

import argparse
import sys
import os
from build_datapack import buildDatapack
from build_loottable import buildLootTable
from minecraft_extract import extractFilesFromJar
from config import loadAndValidateYaml


def chance_calculation(config):
    chance_tattered = ((1 - config['copy-of-copy-chance']) * (1 - config['copy-of-original-chance']) * (1 - config['original-chance'])) * 100
    chance_coc = ((config['copy-of-copy-chance']) * (1 - config['copy-of-original-chance']) * (1 - config['original-chance'])) * 100
    chance_coo = ((config['copy-of-original-chance']) * (1 - config['original-chance'])) * 100
    chance_o = config['original-chance'] * 100
    chance_total = chance_tattered + chance_coc + chance_coo + chance_o
    print(f"Real chances calculation (applying chances sequentially):")
    print(f"Tattered chance:        {chance_tattered:.1f}%")
    print(f"Copy of copy chance:    {chance_coc:.1f}%")
    print(f"Copy of orginal chance: {chance_coo:.1f}%")
    print(f"Orginal chance:         {chance_o:.1f}%")
    print(f"Total:                  {chance_total:.1f}%")


isCompiled = getattr(sys, 'frozen', False)
version = "v2-be%s" % (' (Windows)' if isCompiled else '')
minecraft_version = "1.21.4"

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Optional config filename. (default: %(default)s)', nargs='?', default='config.yaml')
parser.add_argument('-v', '--version', action='version', version=version)
parser.add_argument('-i', '--indent', action='store_true', help="Indent output json files. Overrides config field.")
parser.add_argument('-a', '--append-version', action='store_true', help="Append babel version number to output filename.")
parser.add_argument('-c', '--chance-calc', action='store_true', help="Calculate real chances of various book generations and exit.")

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

    if args.chance_calc:
        chance_calculation(config)

    else:
        # indent arg overrides config field
        if args.indent:
            config['indent-output'] = True

        # Append version alters 'output-filename'
        if args.append_version:
            filename, extension = os.path.splitext(config['output-filename'])
            config['output-filename'] = filename + '_' + version + extension

        extractFilesFromJar(minecraft_version, config['add-lost-libraries'])

        loottable = buildLootTable(config)

        print("\nBuilding data pack...")
        buildDatapack(config, loottable, version, f"data_extracted/{minecraft_version}")
        print("Data pack build complete!\n\nCopy %s to your world's 'datapacks' directory." % config['output-filename'])

except Exception as e:
    print("\nError: " + str(e))

finally:
    if isCompiled and not args.no_wait:
        input("\nPress ENTER or close this window.")
