import yaml
import os


def loadAndValidateYaml(yamlFilePath):
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
        'weights': dict,
    }

    # Define required subfields for 'weights'
    requiredWeights = {
        'stronghold-library': int,
        'woodland-mansion': int,
        'village': int,
        'fishing': int,
        'zombie': int,
    }

    # Always load config.yaml as the base config
    base_config_path = os.path.join(os.path.dirname(yamlFilePath), "config.yaml")
    if not os.path.isfile(base_config_path):
        raise FileNotFoundError(f"Base config file '{base_config_path}' not found.")

    with open(base_config_path, 'r') as file:
        base_data = yaml.safe_load(file) or {}

    # If loading config.yaml itself, treat as before (no defaults)
    if os.path.abspath(yamlFilePath) == os.path.abspath(base_config_path):
        with open(yamlFilePath, 'r') as file:
            data = yaml.safe_load(file) or {}
    else:
        # Overlay user config on top of base config
        with open(yamlFilePath, 'r') as file:
            user_data = yaml.safe_load(file) or {}
        data = base_data.copy()
        data.update(user_data)

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

        # Validate 'weights' field
        if field == 'weights':
            if not isinstance(value, dict):
                raise TypeError(f"Incorrect type for field '{field}'. Expected dict, got {type(value).__name__}.")

            # Check for unrecognized subfields
            for subfield in value:
                if subfield not in requiredWeights:
                    raise ValueError(f"Unrecognized subfield in 'weights': {subfield}")

            # Validate required subfields
            for subfield, subfieldType in requiredWeights.items():
                if subfield not in value:
                    raise ValueError(f"Missing required subfield in 'weights': {subfield}")
                if not isinstance(value[subfield], subfieldType):
                    raise TypeError(f"Incorrect type for subfield '{subfield}' in 'weights'. Expected {subfieldType.__name__}, got {type(value[subfield]).__name__}.")

    return data
