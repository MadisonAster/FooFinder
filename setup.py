from setuptools import setup

setup(
    name='FooFinder',
    version='1.0.0',
    description='A package designed to help you find foo.',
    long_description='FooFinder will walk up to each parent directory from your current module, and look for a module to import with the name you give it.',
    long_description_content_type='text/markdown',
    python_requires='>3.4.0',
    url='https://github.com/MadisonAster/FooFinder',
    author='Madison Aster',
    license='GPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python :: 3',
            ],

    keywords='staticframe pandas numpy immutable array',
    package_dir = {'FooFinder': 'FooFinder'}
    #packages=['FooFinder'],
)