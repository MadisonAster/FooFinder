import unittest

class test_FooFinder(unittest.TestCase):
    def test_1(self):
        from FooFinder import ExampleBaseModule #prove parent imports work
        e = ExampleBaseModule.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
        self.assertNotEqual(e.ExampleAttribute, 'No Dice!')

    def test_2(self):
        from FooFinder import ExampleBaseModule2 #prove child imports work
        e = ExampleBaseModule2.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
        
    def test_3(self):
        from FooFinder import ExampleBaseModule as Ruth #prove child imports work
        e = Ruth.ExampleBaseClass()
        self.assertEqual(e.ExampleAttribute, 'Hello World!')
    
    def test_zzIrregularImport(self):
        import FooFinder #make sure this doesn't throw errors
        import inspect #prove we're only affecting FooFinder imports

    def test_ImportError(self):
        import traceback
        try:
            from FooFinder import ExampleBaseModule3 #prove bad imports fail correctly
        except ImportError:
            pass #ImportError is what we expect

if __name__ == '__main__':
    unittest.main()