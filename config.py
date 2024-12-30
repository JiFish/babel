import yaml


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
        'add-metabox': bool,
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
