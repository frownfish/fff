from distutils.core import setup

setup(name='fff',
      version='0.1',
      description='Fuzzy File Finder',
      author="Jeff Kloosterman",
      url="https://github.com/frownfish/fff",
      packages=['fuzzyfile', 'fuzzyindex'],
      package_dir={'fuzzyfile': 'src/fuzzyfile', 'fuzzyindex': 'src/fuzzyindex' },
      scripts=['src/fffind.py']
      )
