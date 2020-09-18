import sys, os, builtins, inspect
from importlib import machinery
from pprint import pprint

def _import(name, *args, **kwargs):
    if name != 'FooFinder' or not args[2]:
        return original_import(name, *args, **kwargs)
    name = args[2][0]
    frame = inspect.currentframe().f_back
    cwd = os.path.dirname(os.path.abspath(frame.f_globals['__file__'])).replace('\\','/').rstrip('/')
    for i in range(len(cwd.rsplit('/'))):
        folder = cwd.rsplit('/',i)[0]
        path = folder+'/'+name+'.py'
        if os.path.exists(path):
            module = machinery.SourceFileLoader(name, path).load_module()
            sys.modules[name] = module
            globals()[name] = module
            break
    return sys.modules[__name__]

original_import = builtins.__import__
builtins.__import__ = _import
