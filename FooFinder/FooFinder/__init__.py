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

def _get_frame_names():
    frame = inspect.currentframe()
    co_names = ()
    while len(co_names) == 0:
        frame = _framedrag(frame, '_find_and_load_unlocked')
        #context = inspect.getframeinfo(frame).code_context
        co_names = frame.f_code.co_names
        co_varnames = frame.f_code.co_varnames
        f_code = frame.f_code
        #print('co_names', co_names)
        #print('f_code', f_code)
        #print('co_argcount', f_code.co_argcount)
        #print('co_posonlyargcount', f_code.co_posonlyargcount)
        #print('co_kwonlyargcount', f_code.co_kwonlyargcount)
        #print('co_lnotab', f_code.co_lnotab)
        #print('co_nlocals', f_code.co_nlocals)
        #print('co_freevars', f_code.co_freevars)
        #print('co_flags', f_code.co_flags)
        #print('co_firstlineno', f_code.co_firstlineno)
        #print('co_varnames', f_code.co_varnames)
        #print('co_filename', f_code.co_filename)
        #print('co_consts', f_code.co_consts)
        #print('co_code', f_code.co_code)
        #print('f_code', dir(f_code))
    
    if 'FooFinder' in co_varnames: #import FooFinder
        return None, None, None
    for i, name in enumerate(co_names):
        if 'FooFinder' in name:
            break
    pname = co_names[i]
    mname = co_names[i+1]
    #try:
    #    context = inspect.getframeinfo(frame).code_context
    #    code = context[0].rstrip()
    #    print('code', code)
    #except:
    #    pass
    #print('pname, mname', pname, ',', mname)
    #print('-----------------------------------------')
    return frame, pname, mname

def _first_run():
    #replace python's builtin importer
    globals()['original_import'] = builtins.__import__
    builtins.__import__ = _import

    #hack first run by doing some frame dragging because _bootstrap.exec_module doesn't give us *args
    frame, pname, mname = _get_frame_names()
    if frame: #"import FooFinder" shouldn't run _import
        #print('running!', mname)
        args = ('','',(mname,))
        _import(pname, *args, frame=frame)

def _is_ipython():
    return hasattr(builtins, '__IPYTHON__')

def _is_interactive():
    return hasattr(sys, 'ps1')

_first_run()
