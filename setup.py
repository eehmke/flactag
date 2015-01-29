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
DATA=[('imageformats',['C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll'])]
setup(console=['flactag.py'],
  data_files = DATA)
