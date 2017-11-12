import site
import glob
import os
import sys
import re
import os.path
from distutils.sysconfig import get_python_lib
from typing import Optional

def istyped(directory: str) -> bool:
    return os.path.exists(os.path.join(directory, 'py.typed'))

def find_info(pkg_name: str) -> str:
    """
    Checks site-/dist-packages for a package of given name, and reports if it
    is typed or not.
    """
    try:
        pkg_dir = site.getusersitepackages()
        pkg_dirs = site.getsitepackages() + [pkg_dir]
    except AttributeError:
        pkg_dirs = [get_python_lib()]
    for directory in pkg_dirs:
        pkg = os.path.join(directory, pkg_name)
        if os.path.exists(pkg):
            if istyped(pkg):
                print("Package {} has packaged type information.".format(pkg_name))
            else:
                print("Package {} does not support typing.".format(pkg_name))
        elif os.path.exists(pkg + '_stubs'):
            if istyped(pkg+'_stubs'):
                print("Package {} is a stub only package.".format(pkg_name))
            else:
                print("Package {} does not support typing.".format(pkg_name))
        else:
            continue

    


def main():
    if sys.argv[1] == '--help':
        print('Usage: python -m typed_check <pkg>')
    find_info(sys.argv[1])
if __name__ == '__main__':
    main()