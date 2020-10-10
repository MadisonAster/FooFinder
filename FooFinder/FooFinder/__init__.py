import sys, os, builtins, inspect
from importlib import machinery

def _loadmodule(name, path):
    module = machinery.SourceFileLoader(name, path).load_module()
    globals()[name] = module
    sys.modules[name] = module
    return module

def _folderwalker(cwd, down_only=False):
    cwd = cwd.replace('\\','/').rstrip('/')
    if not down_only:
        for i in range(len(cwd.rsplit('/'))):
            root = cwd.rsplit('/',i)[0]
            yield root
    for root, dirs, files in os.walk(cwd):
        dirs.sort() #manipulate dirs iterator to restrain os.walk recursion
        for i, dir in reversed(list(enumerate(dirs))):
            if dir[0] == '.': #.git .hg etc
                del dirs[i]
            elif dir == '__pycache__':
                del dirs[i]
            elif dir.rsplit('.',1)[-1] == 'egg-info':
                del dirs[i]
        yield root.replace('\\','/')

def _find(cwd, name, down_only=False):
    for root in _folderwalker(cwd, down_only=down_only):
        path = os.path.join(root, name).replace('\\','/')
        ppath = os.path.join(path, '__init__.py').replace('\\','/')
        pppath = os.path.join(root, '__init__.py').replace('\\','/')
        path += '.py'
        if os.path.exists(pppath) and os.path.split(root)[1] == name:
            return pppath
        elif os.path.exists(ppath):
            return ppath
        elif os.path.exists(path):
            return path
    else:
        raise ImportError('FooFinder could not find '+name+' searching from '+cwd)

def _is_ipython():
    return hasattr(builtins, '__IPYTHON__')

def _is_interactive():
    return hasattr(sys, 'ps1')
    
def _import(pname, *args, **kwargs):
    if 'FooFinder' not in pname or len(args)< 3 or not args[2]:
        return globals()['_original_import'](pname, *args, **kwargs)
    name = args[2][0]
    if name in globals():
        return sys.modules['FooFinder']
    if 'frame' in kwargs:
        frame = kwargs['frame']
    else:
        frame = inspect.currentframe().f_back    
        if inspect.getframeinfo(frame).function == '_import':
            frame = frame.f_back
    if _is_ipython() or _is_interactive():
        cwd = os.getcwd()
    else:
        cwd = os.path.dirname(os.path.abspath(frame.f_globals['__file__']))
    spname = pname.rsplit('.',1)[-1]
    if spname != 'FooFinder': #relative child imports
        if spname not in globals():
            packpath = _find(cwd, spname)
            _loadmodule(pname, packpath)
        package = globals()[pname]
        if not hasattr(package, name):
            cwd = packpath.rsplit('/',1)[0]
            path = _find(cwd, name, down_only=True)
            _loadmodule(name, path)
            setattr(package, name, globals()[name])
        return package
    else:
        path = _find(cwd, name)
        _loadmodule(name, path)
    return sys.modules['FooFinder']

def _framedrag(frame, functionname):
    while inspect.getframeinfo(frame).function != functionname:
        frame = frame.f_back
    frame = frame.f_back.f_back #go 2 more steps back to the actual function
    return frame

def _get_frame():
    frame = inspect.currentframe()
    co_names = ()
    while len(co_names) == 0:
        frame = _framedrag(frame, '_find_and_load_unlocked')
        co_names = frame.f_code.co_names
    return frame

def _first_run():
    #replace python's builtin importer
    globals()['_original_import'] = builtins.__import__
    builtins.__import__ = _import

    #hack first run by doing some frame dragging because _bootstrap.exec_module doesn't give us *args
    frame = _get_frame()
    if 'FooFinder' in frame.f_code.co_varnames: #import FooFinder
        return
    for i, name in enumerate(frame.f_code.co_names):
        if 'FooFinder' in name:
            break
    pname = frame.f_code.co_names[i]
    mname = frame.f_code.co_names[i+1]
    args = ('','',(mname,))
    return _import(pname, *args, frame=frame)

_first_run()
