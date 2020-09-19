import sys, os, builtins, inspect, traceback
from importlib import machinery
from pprint import pprint

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
            dirs.sort()
            path = root+'/'+name+'.py'
            if os.path.exists(path):
                module = _loadmodule(name, path)
                break
    return sys.modules['FooFinder']

#replace builtin importer so the ugly hack below only has to run once
original_import = builtins.__import__
builtins.__import__ = _import

##this hack is lame...
frame = inspect.currentframe()
while inspect.getframeinfo(frame).function != '_find_and_load':
    frame = frame.f_back
frame = frame.f_back #go 1 more step back to get calling function
context = inspect.getframeinfo(frame).code_context[0] #get line that called FooFinder
mname = context.split('from FooFinder import ',1)[-1].split(' ')[0].split('#')[0] #split on syntax
args = ('','',(mname,))
_import('FooFinder', *args)

