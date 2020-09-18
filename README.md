![PyPI](https://img.shields.io/pypi/v/FooFinder)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FooFinder)
[![Build Status](https://travis-ci.org/MadisonAster/FooFinder.svg?branch=master)](https://travis-ci.org/MadisonAster/FooFinder)


A package designed to help you find foo. FooFinder makes relative imports easy with this one simple trick. 

## Installation:
```
pip install FooFinder
```

## Usage:
```
from FooFinder import MySuperAwesomeModule
```

FooFinder will walk up to each parent directory, and down to each child directory, from the location of your current module. FooFinder will import and return the first module that it finds with the name you give it.
