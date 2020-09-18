import unittest

class test_FooFinder(unittest.TestCase):
    def test_1(self):
        import FooFinder
        import inspect #prove we're only affecting FooFinder imports
        from FooFinder import ExampleBaseModule
        i = ExampleBaseModule.ExampleBaseClass()
        self.assertEqual(i.ExampleAttribute, 'Hello World!')

if __name__ == '__main__':
    unittest.main()