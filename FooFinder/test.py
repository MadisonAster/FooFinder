import unittest
import sys, builtins, copy

class test_FooFinder(unittest.TestCase):
    def setUp(self):
        self.original_import = builtins.__import__
        self.modulekeys = list(sys.modules.keys())
        if 'FooFinder' in sys.modules: #just in case
            del sys.modules['FooFinder']

    def tearDown(self):
        builtins.__import__ = self.original_import
        for key in reversed(list(sys.modules.keys())):
            if key not in self.modulekeys:
                del sys.modules[key]
    
    def test_UpstreamModules(self):
        from FooFinder import ExampleBaseModule #prove upstream imports work
        e = ExampleBaseModule.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
        self.assertNotEqual(e.ExampleAttribute, 'No Dice!')

    def test_DownstreamModules(self):
        from FooFinder import ExampleBaseModule2 #prove downstream imports work
        e = ExampleBaseModule2.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
    
    def test_UpstreamPackages(self):
        from FooFinder import ExamplePackage #prove upstream packages work
        self.assertEqual(ExamplePackage.ExampleAttribute, 'Hello Packages!')
    
    def test_DownstreamPackages(self):
        from FooFinder import TestPackage #prove downstream packages work
        self.assertEqual(TestPackage.ExampleAttribute1, 'Hello Downstream Packages!')
    
    def test_DownstreamTestCall(self):
        from FooFinder import PackageTestModule
        PackageTestModule.test_ParentPackages()
    
    def test_NameSpaces(self):
        from FooFinder import ExampleBaseModule as Ruth #prove namespaces work
        e = Ruth.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
    
    def test_IrregularImport(self):
        import FooFinder #make sure this doesn't throw errors
        import inspect #prove we're only affecting FooFinder imports
        
    def test_RelativeChildImports(self):
        from FooFinder.ExamplePackage import ExampleChildModule
        e = ExampleChildModule.ExamplePackageClass()
        self.assertEqual(e.ExampleAttribute, 'Hello Relative children!')
        
    def test_RelativeChildImports2(self):
        from FooFinder.ExampleBaseModule2 import ExampleChildModule2
        e = ExampleChildModule2.ExamplePackageClass()
        self.assertEqual(e.ExampleAttribute, 'Hello Relative children2!')

    def test_ImportError(self):
        import traceback
        try:
            from FooFinder import ExampleBaseModule3 #prove bad imports fail correctly
        except ImportError:
            pass #ImportError is what we expect

if __name__ == '__main__':
    unittest.main()