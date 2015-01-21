import distutils
from distutils.core import setup
import py2exe

distutils.core.setup (
options = {
  "py2exe": {
    "compressed": 1,
    "optimize": 2,
    "dll_excludes": [ "MSVCP90.dll"]
  }
}
)

setup(console=['flactag.py'])

