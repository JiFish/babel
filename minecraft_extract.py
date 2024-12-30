import os
import platform
from pathlib import Path
import zipfile
from progress_bar import printProgressBar


def get_minecraft_jar_path(version: str) -> Path:
    """
    Locate the Minecraft .jar file for a given version across different operating systems.

    Args:
        version (str): The Minecraft version to search for.

    Returns:
        Path: Path to the Minecraft .jar file if found, or None if not found.
    """
    # Determine the Minecraft directory based on the OS
    system = platform.system()

    if system == "Windows":
        minecraft_dir = Path(os.getenv("APPDATA")) / ".minecraft" / "versions"
    elif system == "Darwin":  # macOS
        minecraft_dir = Path.home() / "Library" / "Application Support" / "minecraft" / "versions"
    elif system == "Linux":
        minecraft_dir = Path.home() / ".minecraft" / "versions"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

    # Build the expected jar file path
    version_dir = minecraft_dir / version
    jar_file = version_dir / f"{version}.jar"

    # Check if the jar file exists
    if jar_file.is_file():
        return jar_file
    else:
        print(f"Minecraft jar file for version {version} not found. You must have Minecraft v{version} installed to use the tool.")
        os._exit(1)


def extract_files_from_jar(jar_path: Path, sources, destination: Path, title) -> None:
    """
    Extract specific files or all files matching a pattern from a Minecraft .jar file.

    Args:
        jar_path (Path): Path to the .jar file.
        source_pattern (str): The file or pattern to extract (e.g., "data/loot_tables/wool.json" or "data/loot_tables/*").
        destination (Path): The destination directory to extract files to.

    Returns:
        None
    """
    if not jar_path.is_file():
        raise FileNotFoundError(f"Jar file not found: {jar_path}")

    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(jar_path, 'r') as jar:
        # List of all files in the jar
        jar_files = jar.namelist()

        if type(sources) == list:
            # Handle list extraction
            files_to_extract = sources
        elif sources.endswith("/*"):
            # Handle wildcard extraction
            base_pattern = sources[:-2]
            files_to_extract = [f for f in jar_files if f.startswith(base_pattern)]
        else:
            # Handle single file extraction
            files_to_extract = [sources]

        if not files_to_extract:
            print(f"No files matching '{sources}' found in {jar_path}.")
            return

        totalfiles = len(files_to_extract)
        i = 0
        for file in files_to_extract:
            i += 1
            target_path = destination / Path(file).name
            with jar.open(file) as source_file:
                with open(target_path, 'wb') as target_file:
                    target_file.write(source_file.read())

            printProgressBar(i, totalfiles, prefix=title, length=40, decimals=0)


def extractFilesFromJar(minecraft_version, include_recipes):
    checkPath = ("/base_recipe" if include_recipes else "/base_loot_tables")
    if Path(f"data_extracted/{minecraft_version}/{checkPath}").exists():
        print(f"Minercaft {minecraft_version} files already extracted. Skipping...\n")
        return

    jar_path = get_minecraft_jar_path(minecraft_version)
    print(f"Found Minecraft {minecraft_version} jar file: {jar_path}")

    if include_recipes:
        destination = Path(f"data_extracted/{minecraft_version}/base_recipe")
        source_pattern = 'data/minecraft/recipe/*'
        extract_files_from_jar(jar_path, source_pattern, destination, "Extracting recipies...")

    destination = Path(f"data_extracted/{minecraft_version}/base_loot_tables")
    sources = [
        'data/minecraft/loot_table/gameplay/fishing/treasure.json',
        'data/minecraft/loot_table/entities/zombie.json',
        'data/minecraft/loot_table/chests/stronghold_library.json',
        'data/minecraft/loot_table/chests/woodland_mansion.json',
        'data/minecraft/loot_table/chests/village/village_desert_house.json',
        'data/minecraft/loot_table/chests/village/village_plains_house.json',
        'data/minecraft/loot_table/chests/village/village_savanna_house.json',
        'data/minecraft/loot_table/chests/village/village_snowy_house.json',
        'data/minecraft/loot_table/chests/village/village_taiga_house.json',
    ]
    extract_files_from_jar(jar_path, sources, destination, "Extracting base loot tables...")

    print("")
