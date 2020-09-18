import sys, os, builtins, inspect, traceback
from importlib import machinery

def _loadmodule(name, path):
    module = machinery.SourceFileLoader(name, path).load_module()
    sys.modules[name] = module
    globals()[name] = module
    return module

def _import(name, *args, **kwargs):
    if name != 'FooFinder' or not args[2]:
        return original_import(name, *args, **kwargs)
    name = args[2][0]
    if name in globals():
        return sys.modules['FooFinder']
    elif name in sys.modules:
        globals()[name] = sys.modules[name]
        return sys.modules['FooFinder']
    frame = inspect.currentframe().f_back
    cwd = os.path.dirname(os.path.abspath(frame.f_globals['__file__'])).replace('\\','/').rstrip('/')
    for i in range(len(cwd.rsplit('/'))):
        folder = cwd.rsplit('/',i)[0]
        path = folder+'/'+name+'.py'
        if os.path.exists(path):
            module = _loadmodule(name, path)
            break
    else:
        for root, dirs, files in os.walk(cwd):
            path = root+'/'+name+'.py'
            if os.path.exists(path):
                module = _loadmodule(name, path)
                break
    return sys.modules['FooFinder']

original_import = builtins.__import__
builtins.__import__ = _import
