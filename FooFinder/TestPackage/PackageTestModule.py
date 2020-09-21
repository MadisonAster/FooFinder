import unittest

def test_ParentPackages():
    from FooFinder import TestPackage
    assert TestPackage.ExampleAttribute2 == 'Hello Parent Packages!'
    
    