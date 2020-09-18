import unittest

class test_FooFinder(unittest.TestCase):
    def test_1(self):
        from FooFinder import ExampleBaseModule
        import inspect #prove we're only affecting FooFinder imports
        i = ExampleBaseModule.ExampleBaseClass()
        self.assertEqual(i.ExampleAttribute, 'Hello World!')

if __name__ == '__main__':
    unittest.main()