import json
import copy
from glob import glob
from progress_bar import printProgressBar

item_template = {
    "type": "minecraft:item",
    "name": "minecraft:knowledge_book",
    "functions": [
        {
            "function": "minecraft:set_components",
            "components": {
                "minecraft:recipes": [],
                "minecraft:lore": []
            }
        }
    ]
}

def parse_recipe_file(recp):
    """Parses a recipe file and returns its JSON data and name."""
    name = recp.replace('\\', '/').split('/')[-1][:-5]  # Extract file name without extension
    with open(recp) as jsonFile:
        recp_json = json.load(jsonFile)
    return name, recp_json


def should_skip_recipe(recp_json):
    """Determines if a recipe should be skipped based on its output and keys."""
    if recp_json['type'] not in ['minecraft:crafting_shaped', 'minecraft:crafting_shapeless']:
        return True

    if recp_json['result']['id'].startswith("minecraft:waxed"):
        return True

    if recp_json['type'] == 'minecraft:crafting_shaped':
        output_item = recp_json['result']['id']
        for items in recp_json['key'].values():
            if isinstance(items, str):
                items = [items]
            if output_item in items:
                return True
    return False


def update_loot_pool(newpool, name, group_name):
    """Updates the loot pool with a new or existing group."""
    if group_name not in newpool:
        newitem = copy.deepcopy(item_template)
        newitem["functions"][0]["components"]["minecraft:recipes"].append("minecraft:" + name)
        newitem["functions"][0]["components"]["minecraft:lore"].append(f'"{group_name.replace("_", " ").title()}"')
        newpool[group_name] = newitem
    else:
        newpool[group_name]["functions"][0]["components"]["minecraft:recipes"].append("minecraft:" + name)


def process_recipes(recipes):
    """Processes all recipes and updates the loot pool."""
    newpool = {}
    total_recipes = len(recipes)

    for i, recp in enumerate(recipes, start=1):
        printProgressBar(i, total_recipes, "Creating knowledge books loot table...", length=40, decimals=0)
        name, recp_json = parse_recipe_file(recp)

        if should_skip_recipe(recp_json):
            continue

        group_name = recp_json.get('group', name)
        update_loot_pool(newpool, name, group_name)

    return newpool


def buildKnowledgeBooksTable(extracted_data_directory):
    """Creates the knowledge books loot table."""
    recipes = glob(f"{extracted_data_directory}/base_recipe/*.json")
    newpool = process_recipes(recipes)
    print(f"{len(newpool)} knowlege books created.")
    return {
        "pools": [
            {
                "rolls": 1,
                "entries": list(newpool.values())
            }
        ]
    }
