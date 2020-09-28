![PyPI](https://img.shields.io/pypi/v/FooFinder)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FooFinder)
[![Build Status](https://travis-ci.org/MadisonAster/FooFinder.svg?branch=master)](https://travis-ci.org/MadisonAster/FooFinder)


*A package designed to help you find foo. FooFinder makes relative imports easy with this one simple trick!*

---

## Installation:
```
pip install FooFinder
```

## Usage:
```
from FooFinder import MySuperAwesomeModule
```

---

### ***FooFinder will walk up to each parent directory, and down to each child directory, from the location of your current module. FooFinder will import and return the first module or package that it finds with the name you give it.***

---

## Other ways to use FooFinder:

#### Using a namespace:
```
from FooFinder import CoolStuff as SuperCoolStuff
```


#### Importing a package:
```
from FooFinder import MyNiftyPackage
```

---

### ***FooFinder can find the package you're currently in, a package from a parent directory, or a package from a child directory. Modules within packages will be found as if they were folders.***

---

#### Using a parent package as a reference point:
```
ParentFolder/
    __init__.py
    SubFolder1/
        TargetModule.py #<- and you want to import this
    SubFolder2/
        SubSubFolder/
            CurrentModule.py #<- you are here

from FooFinder.ParentFolder import TargetModule
```        

#### Using a neighboring package as a reference point:
```   
ParentFolder/
    SubFolder1/
        __init__.py
        SubSubFolder/
            TargetModule.py #<- and you want to import that
    SubFolder2/
        SubSubFolder/
            CurrentNotebook.ipynb #<- you are here

from FooFinder.SubFolder1 import TargetModule
from FooFinder.SubFolder1 import SomePackageAttribute
```

#### Using a root module as a reference point:
```
ParentFolder/
    RootModule.py
    SubFolder1/
        SubSubFolder/
            TargetPackage/ #<- and you want to import this
                __init__.py
    SubFolder2/
        SubSubFolder/
            CurrentModule.py #<- you are here
        
from FooFinder.RootModule import TargetPackage
```

---

*See the [test module](https://github.com/MadisonAster/FooFinder/blob/master/FooFinder/test.py) for example usage and complete test coverage.*