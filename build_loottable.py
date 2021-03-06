import json
import os

directory = 'books/'
entries = [];

for file in os.listdir(directory):
    path = os.path.join(directory, file)
    with open(path, 'r') as thisfile:
        book = json.load(thisfile)
    book['generation'] = 3

    entries.append({
        "type": "item",
        "name": "minecraft:written_book",
        "weight": 1,
        "functions": [
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps(book)
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':2}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.3
                    }
                ]
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':1}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.01
                    }
                ]
            },
            {
                "function": "minecraft:set_nbt",
                "tag": json.dumps({'generation':0}),
                "conditions": [
                    {
                        'condition': "random_chance",
                        'chance': 0.003
                    }
                ]
            }
        ]
    })


loottable = {
    'pools': [
        {
            'rolls': 1,
            'entries': entries
        }
    ]
}

if __name__ == '__main__':
    print(json.dumps(loottable, indent=4))
