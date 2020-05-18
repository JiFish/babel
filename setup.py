from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = ['email', 'html', 'http', 'logging', 'pydoc_data', 'unittest', 'urllib', 'xml'], include_files = ['books/', 'base_loot_tables/', 'README.md'])


base = 'Console'

executables = [
    Executable('babel.py', base=base)
]

setup(name='babel',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
