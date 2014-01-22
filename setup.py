from distutils.core import setup

setup(name='fff',
      version='0.1',
      description='Fuzzy File Finder',
      author="Jeff Kloosterman",
      url="https://github.com/frownfish/fff",
      packages=['fff'],
      package_dir={'fff': 'src/fff'},
      scripts=['src/fffind.py']
      )
