import sys, os, builtins, inspect
from importlib import machinery

def _loadmodule(name, path):
    module = machinery.SourceFileLoader(name, path).load_module()
    globals()[name] = module
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
        path = path+'.py'
        if os.path.exists(path):
            return path
        if os.path.exists(ppath):
            return ppath
    else:
        raise ImportError('FooFinder could not find '+name+' searching from '+cwd)

def _import(pname, *args, **kwargs):
    if 'FooFinder' not in pname or not args[2]:
        return globals()['original_import'](pname, *args, **kwargs)
    name = args[2][0]
    if name in globals():
        return sys.modules['FooFinder']
    if 'frame' in kwargs:
        frame = kwargs['frame']
    else:
        frame = inspect.currentframe().f_back
    try:
        cwd = os.path.dirname(os.path.abspath(frame.f_globals['__file__']))
    except:
        cwd = os.getcwd() #iPython needs this
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
    while inspect.getframeinfo(frame).function != '_find_and_load':
        frame = frame.f_back
    frame = frame.f_back #go 1 more step back to the actual function
    return frame

def _get_frame_code():
    frame = inspect.currentframe()
    context = None
    while context == None:
        frame = _framedrag(frame, '_find_and_load')
        context = inspect.getframeinfo(frame).code_context
    code = context[0].rstrip()
    return frame, code

def _parse_code(code):
    #parsing these is hacky and lame...
    pname = code.split('from ',1)[-1].split(' import',1)[0]
    mname = code.split(' import ',1)[-1].split(' ')[0].split('#')[0].rstrip()
    return pname, mname

def _first_run():
    #replace python's builtin importer
    globals()['original_import'] = builtins.__import__
    builtins.__import__ = _import

    #hack first run by doing some frame dragging because _bootstrap.exec_module doesn't give us *args
    frame, code = _get_frame_code() #get line of code that called FooFinder
    pname, mname = _parse_code(code) #parse package and module names from code
    if mname != 'FooFinder': #"import FooFinder" shouldn't run _import
        args = ('','',(mname,))
        _import(pname, *args, frame=frame)

_first_run()
