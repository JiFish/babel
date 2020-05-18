import json
import os

directory = 'books/'
entries = [];

for file in os.listdir(directory):
    path = os.path.join(directory, file)
    with open(path, 'r') as myfile:
        lines = myfile.readlines()
    if (len(lines) < 3):
        print("Book "+file+" too short. Minimum 3 lines for Author, Title and Page 1. Skipping.")
        continue
    book = {}
    book['author'] = lines[0].strip()
    book['title'] = lines[1].strip()
    book['generation'] = 3
    book['pages'] = []
    lines = lines[2:]
    for l in lines:
        book['pages'].append('{"text":"'+l.replace('"','\"').strip()+'"}')
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