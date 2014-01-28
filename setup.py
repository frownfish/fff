'''
Setup script for FuzzyFileFinder.
'''

import setuptools

from fff import __project__, CLI, __version__

README = 'README.md'


setuptools.setup(name=__project__,
                 version=__version__,

                 description='Fuzzy File Finder.',
                 url="https://github.com/frownfish/fff",

                 author='Jeff Kloosterman',
                 author_email='kloosterman.jeff@gmail.com',

                 packages=setuptools.find_packages(),

                 entry_points={'console_scripts': [CLI + ' = fff.fffind:main']},
                 license='MIT',

                 long_description=open(README).read(),
                 install_requires=[]
                 )
