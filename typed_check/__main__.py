import site
import glob
import os
import sys
import re
import os.path
from typing import Optional

TYPED_PATTERN = r'Typed: (.*)\n'

def check_metadata(path: str) -> Optional[str]:
    """Returns the static typing metadata information. This is either
    "inline", "stubs", or None
    """
    with open(path) as f:
        for line in reversed(f.readlines()):
            info = re.search(TYPED_PATTERN, line)
            if info:
                return info.group(1)

def find_info(pkg_name: str) -> str:
    """
    Gets path to metadata file installed in either the OS sitepackages or the
    user sitepackages. It returns the path to either *-*.dist-info/METADATA or
    *-*.egg-info
    """
    paths = []
    for dir in site.getsitepackages() + [site.getusersitepackages()]:
        paths.extend(glob.glob(os.sep.join([dir, f'{pkg_name}-*.*-info'])))
    assert len(paths) > 0, f"Did not find metadata for package {pkg_name}"
    assert len(paths) == 1, f"Conflicting packages found: {paths}"
        
    path = paths[0]
    typed: Optional[str] = None
    if os.path.isfile(path) and path.endswith(".egg-info"):
        # .egg-info file, just read it
        typed = check_metadata(path)
    elif os.path.isdir(path) and path.endswith(".dist-info"):
        # .dist-info folder, read the METADATA file
        meta_file = os.sep.join([path, "METADATA"])
        assert os.path.isfile(meta_file), f"Could not find a METADATA file in {path}"
        typed = check_metadata(meta_file)
    if typed == 'inline':
        print(f'Package {pkg_name} has inline type annotations')
    elif typed == 'stubs':
        print(f'Package {pkg_name} has stub files')
    elif typed is None:
        print(f'Package {pkg_name} is not typed')


def main():
    if sys.argv[1] == '--help':
        print('Usage: python -m typed_check <pkg>')
    find_info(sys.argv[1])
if __name__ == '__main__':
    main()