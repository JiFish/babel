from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [],
                    excludes = ['email', 'html', 'http', 'logging', 'pydoc_data', 'unittest', 'urllib', 'xml'],
                    include_files = [
                        'books/',
                        'base_loot_tables/',
                        'extras/',
                        'config.yaml',
                        'config_no_copying.yaml',
                        'config_no_zombies.yaml',
                        'config_only_chests.yaml',
                        'config_with_recipe.yaml',
                        'README.md',
                        'LICENSE.txt'
                    ])

base = 'Console'

executables = [
    Executable('babel.py', base=base)
]

setup(name='babel',
      version = '1.1',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
