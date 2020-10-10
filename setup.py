import os
from setuptools import setup

def readme():
    with open('README.md', 'r') as file:
        filetext = file.read()
    return filetext
setup(
    name='FooFinder',
    version='3.0.4',
    description='A package designed to help you find foo.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    python_requires='>3.5.0',
    url='https://github.com/MadisonAster/FooFinder',
    author='Madison Aster',
    author_email='info@MadisonAster.com',
    license='LGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            ],

    keywords='staticframe pandas numpy immutable array',
    package_dir = {'': 'FooFinder'},
    packages=['FooFinder'],
)