import sys, os, builtins, inspect, traceback
from importlib import machinery

def _loadmodule(name, path):
    module = machinery.SourceFileLoader(name, path).load_module()
    sys.modules[name] = module
    globals()[name] = module
    return module

def _folderwalker(cwd):
    cwd = cwd.replace('\\','/').rstrip('/')
    for i in range(len(cwd.rsplit('/'))):
        root = cwd.rsplit('/',i)[0]
        yield root
    else:
        for root, dirs, files in os.walk(cwd):
            dirs.sort() #some systems return unsorted directory listings
                        #python uses the dirs iterator to do it's walking
                        #so we have to sort if we want to find things in 
                        #order on all systems
            folder = os.path.split(root)[-1]
            if folder in ['__pycache__']:
                continue
            if folder[0] == '.': #.git .hg etc
                continue
            if folder.rsplit('.',1)[-1] == 'egg-info':
                continue
            yield root
            
def _import(name, *args, **kwargs):
    if name != 'FooFinder' or not args[2]:
        return original_import(name, *args, **kwargs)
    name = args[2][0]
    if name in globals():
        return sys.modules['FooFinder']
    elif name in sys.modules:
        globals()[name] = sys.modules[name]
        return sys.modules['FooFinder']
    if 'frame' in kwargs:
        frame = kwargs['frame']
    else:
        frame = inspect.currentframe().f_back
    cwd = os.path.dirname(os.path.abspath(frame.f_globals['__file__']))
    for root in _folderwalker(cwd):
        path = os.path.join(root, name)
        ppath = os.path.join(path, '__init__.py')
        path = path+'.py'
        if os.path.exists(path):
            _loadmodule(name, path)
            break
        if os.path.exists(ppath):
            _loadmodule(name, ppath)
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
if mname != '': #import FooFinder shouldn't run _import
    args = ('','',(mname,))
    _import('FooFinder', *args, frame=frame)

