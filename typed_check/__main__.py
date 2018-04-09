import site
import os
import sys
import os.path
from distutils.sysconfig import get_python_lib


def istyped(directory: str) -> bool:
    return os.path.exists(os.path.join(directory, 'py.typed'))


def find_info(pkg_name: str) -> None:
    """
    Checks site-/dist-packages for a package of given name, and reports if it
    is typed or not.
    """
    try:
        pkg_dir = site.getusersitepackages()
        pkg_dirs = site.getsitepackages() + [pkg_dir]
    except AttributeError:
        print('Cannot use site module, falling back to sysconfig.')
        pkg_dirs = [get_python_lib()]
    inline = False
    stub = False
    exists = False
    
    for pkg_dir in pkg_dirs:
        stub_name = pkg_name + '-stubs'
        typed_file = os.path.join(pkg_dir, pkg_name, 'py.typed')
        stub_dir = os.path.join(pkg_dir, stub_name)
        if os.path.isdir(os.path.join(pkg_dir, pkg_name)):
            exists = True
        if os.path.isdir(stub_dir):
            stub = True
        elif os.path.isfile(typed_file):
            inline = True
    if stub:
        print("Package {} is a stub only package.".format(pkg_name))
    elif inline:
        print("Package {} has inline type information.".format(pkg_name))
    elif exists:
        print("Package {} does not support typing.".format(pkg_name))
    else:
        print("Could not find package '{}'.".format(pkg_name))

def main():
    if sys.argv[1] == '--help':
        print('Usage: python -m typed_check <package name>')
        sys.exit(0)
    find_info(sys.argv[1])


if __name__ == '__main__':
    main()
